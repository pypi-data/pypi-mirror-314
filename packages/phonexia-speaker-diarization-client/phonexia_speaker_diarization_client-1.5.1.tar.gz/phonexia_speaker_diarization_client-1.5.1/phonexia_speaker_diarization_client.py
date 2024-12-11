#!/usr/bin/python3

import argparse
import fnmatch
import logging
import os
import sys
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

import google.protobuf.duration_pb2
import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.speaker_diarization.v1.speaker_diarization_pb2 as diarization
import phonexia.grpc.technologies.speaker_diarization.v1.speaker_diarization_pb2_grpc as diarization_grpc
import soundfile
from google.protobuf.json_format import MessageToJson
from phonexia.grpc.common.core_pb2 import RawAudioConfig

CHUNK_SIZE = 1024 * 1024


class speaker_diarization_client:
    def __init__(
        self,
        host: str,
        use_ssl: bool,
        max_speakers: Optional[int] = None,
        total_speakers: Optional[int] = None,
        output_format="lab",
        metadata: Optional[list] = None,
    ):
        if use_ssl:
            logging.info("Connecting to %s via secure channel", host)
            credentials = grpc.ssl_channel_credentials()
            self.channel = grpc.secure_channel(host, credentials)
        else:
            logging.info("Connecting to %s via insecure channel", host)
            self.channel = grpc.insecure_channel(host)

        self.max_speakers = max_speakers
        self.total_speakers = total_speakers
        logging.info(
            "Using max_speakers=%s and total_speakers=%s",
            self.max_speakers,
            self.total_speakers,
        )
        self.diarize_stub = diarization_grpc.SpeakerDiarizationStub(self.channel)
        if output_format not in {"lab", "rttm", "json"}:
            raise ValueError("Unsupported output format")
        self.format = output_format
        self.metadata = metadata

    @staticmethod
    def time_to_duration(time: float) -> Optional[google.protobuf.duration_pb2.Duration]:
        if time is None:
            return None
        duration = google.protobuf.duration_pb2.Duration()
        duration.seconds = int(time)
        duration.nanos = int((time - duration.seconds) * 1e9)
        return duration

    def file_to_request(
        self,
        file: Path,
        start: float,
        end: float,
        use_raw_audio: bool,
    ) -> Iterator[diarization.DiarizeRequest]:
        time_range = phx_common.TimeRange(
            start=self.time_to_duration(start), end=self.time_to_duration(end)
        )

        total_speakers = self.total_speakers if self.total_speakers is not None else None
        max_speakers = self.max_speakers if self.max_speakers is not None else None
        config = diarization.DiarizeConfig(max_speakers=max_speakers, total_speakers=total_speakers)

        if use_raw_audio:
            with soundfile.SoundFile(file) as r:
                raw_audio_config = RawAudioConfig(
                    channels=r.channels,
                    sample_rate_hertz=r.samplerate,
                    encoding=RawAudioConfig.AudioEncoding.PCM16,
                )

                for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                    logging.debug("Sending chunk of size %d samples", len(data))
                    yield diarization.DiarizeRequest(
                        audio=phx_common.Audio(
                            content=data.flatten().tobytes(),
                            time_range=time_range,
                            raw_audio_config=raw_audio_config,
                        ),
                        config=config,
                    )
                    time_range = None
                    raw_audio_config = None
                    config = None
        else:
            with open(file, "rb") as f:
                while chunk := f.read(CHUNK_SIZE):
                    logging.debug("Sending chunk of size %d bytes", len(chunk))
                    yield diarization.DiarizeRequest(
                        audio=phx_common.Audio(content=chunk, time_range=time_range), config=config
                    )
                    time_range = None
                    config = None

    @staticmethod
    def save_response_lab(response: diarization.DiarizeResponse, output):
        def to_htk(sec: float):
            return int(round(sec * 10**7, ndigits=0))

        for segment in response.segments:
            output.write(
                "{start:d} {end:d} {speaker:d}\n".format(  # noqa: UP032
                    start=to_htk(segment.start_time.ToTimedelta().total_seconds()),
                    end=to_htk(segment.end_time.ToTimedelta().total_seconds()),
                    speaker=int(segment.speaker_id) + 1,
                )
            )

    @staticmethod
    def save_response_rttm(response: diarization.DiarizeResponse, file: Path, output):
        for segment in response.segments:
            beg = segment.start_time.ToTimedelta().total_seconds()
            end = segment.end_time.ToTimedelta().total_seconds()
            size = end - beg
            output.write(
                f"SPEAKER {file.stem} 1 {beg:.2f} {size:.2f} <NA> <NA>"
                f" {int(segment.speaker_id) + 1} <NA>\n"
            )

    def send_diarize_request(
        self, request: Iterator[diarization.DiarizeRequest]
    ) -> diarization.DiarizeResponse:
        return self.diarize_stub.Diarize(request, metadata=self.metadata)

    def process_file(
        self,
        in_file: Path,
        use_raw_audio: bool,
        start: Optional[float] = None,
        end: Optional[float] = None,
        output_file: Optional[Path] = None,
    ):
        logging.info("%s -> %s", in_file, output_file if output_file else "stdout")

        response = self.send_diarize_request(
            self.file_to_request(file=in_file, start=start, end=end, use_raw_audio=use_raw_audio)
        )

        with (
            open(output_file, mode="w", encoding="utf8") if output_file else nullcontext(sys.stdout)
        ) as output:
            if self.format == "lab":
                self.save_response_lab(response, output)
            elif self.format == "rttm":
                self.save_response_rttm(response, in_file, output)
            elif self.format == "json":
                output.write(MessageToJson(response, always_print_fields_with_no_presence=True))

    def process_dir(
        self,
        in_dir: Path,
        use_raw_audio: bool,
        start: Optional[float] = None,
        end: Optional[float] = None,
        output: Optional[Path] = None,
        input_suffix: str = "wav",
    ):
        if output is not None and not output.exists():
            os.mkdir(output)

        logging.info("Scanning directory %s for *.%s", os.path.abspath(in_dir), input_suffix)
        files = os.listdir(in_dir)
        filtered_files = [f for f in files if fnmatch.fnmatch(f, f"*.{input_suffix}")]
        logging.info("Found %d files", len(filtered_files))
        for file in filtered_files:
            in_file = in_dir / file
            out_file = (
                None if output is None else (Path(output) / file).with_suffix("." + self.format)
            )
            self.process_file(
                in_file=in_file,
                start=start,
                end=end,
                output_file=out_file,
                use_raw_audio=use_raw_audio,
            )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Speaker Diarization gRPC client. Identifies speakers in input audio and returns"
            " segments with timestamps for each speaker."
        )
    )
    parser.add_argument(
        "-H",
        "--host",
        default="localhost:8080",
        help="Phonexia Speech Engine gRPC API server host",
    )
    parser.add_argument("--use_ssl", action="store_true", default=False, help="Use SSL connection")
    parser.add_argument(
        "-F",
        "--out_format",
        default="lab",
        choices=["lab", "rttm", "json"],
        help="Output format",
    )
    speakers = parser.add_mutually_exclusive_group(required=False)
    speakers.add_argument(
        "--total_speakers",
        type=int,
        help="Exact number of speakers in recording",
    )
    speakers.add_argument(
        "--max_speakers",
        type=int,
        help="Maximum number of speakers in recording",
    )
    parser.add_argument(
        "--metadata",
        metavar="key=value",
        nargs="+",
        type=lambda x: tuple(x.split("=")),
        help="Custom client metadata",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
        help="Logging level",
    )
    input_options = parser.add_mutually_exclusive_group(required=True)
    input_options.add_argument("-i", "--in_file", type=Path, help="Path to audio file")
    input_options.add_argument(
        "-d", "--in_dir", type=Path, help="Path to directory containing audio files"
    )
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")
    parser.add_argument(
        "-e",
        "--in_extension",
        default="wav",
        help="Input extension of files in directory.",
    )
    output_options = parser.add_mutually_exclusive_group(required=False)
    output_options.add_argument(
        "-o",
        "--out_file",
        type=Path,
        help="Location the output will be stored into.",
    )
    output_options.add_argument(
        "-D",
        "--out_dir",
        type=Path,
        help="Directory in which the output will be stored.",
    )
    parser.add_argument("--use_raw_audio", action="store_true", help="Send a raw audio")

    args = parser.parse_args()

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.\n")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.\n")

    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.\n")

    if args.max_speakers is not None and args.max_speakers == 0:
        raise ValueError("Option 'max_speakers' must be larger than 0.\n")

    if args.out_file and args.in_dir:
        raise ValueError("'-o' option can not be used with '-d'.\n")

    if args.out_dir and args.in_file:
        raise ValueError("'-D' option can not be used with '-i'.\n")

    if args.in_file and not os.path.isfile(args.in_file):
        raise ValueError(f"No such file or directory '{args.in_file}'.\n")

    if args.in_dir and not os.path.isdir(args.in_dir):
        raise ValueError(f"No such file or directory '{args.in_dir}'.\n")

    return args


def main():
    args = parse_arguments()

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        client = speaker_diarization_client(
            args.host,
            args.use_ssl,
            args.max_speakers,
            args.total_speakers,
            args.out_format,
            args.metadata,
        )

        start_time = datetime.now()
        if args.in_file:
            client.process_file(
                in_file=args.in_file,
                start=args.start,
                end=args.end,
                output_file=args.out_file,
                use_raw_audio=args.use_raw_audio,
            )

        elif args.in_dir:
            client.process_dir(
                in_dir=args.in_dir,
                start=args.start,
                end=args.end,
                output=args.out_dir,
                input_suffix=args.in_extension,
                use_raw_audio=args.use_raw_audio,
            )

        logging.debug(f"Elapsed time {(datetime.now() - start_time)}")

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
