import argparse
import json
import logging
import pathlib
from typing import Iterator, Optional

import google.protobuf.duration_pb2
import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import soundfile
from google.protobuf.json_format import MessageToDict
from phonexia.grpc.common.core_pb2 import RawAudioConfig
from phonexia.grpc.technologies.voice_activity_detection.v1.voice_activity_detection_pb2 import (
    DetectRequest,
    DetectResponse,
)
from phonexia.grpc.technologies.voice_activity_detection.v1.voice_activity_detection_pb2_grpc import (
    VoiceActivityDetectionStub,
)


def time_to_duration(time: Optional[float]) -> Optional[
    google.protobuf.duration_pb2.Duration]:
    if time is None:
        return None
    duration = google.protobuf.duration_pb2.Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
        file: str,
        start: Optional[float],
        end: Optional[float],
        use_raw_audio: bool,
) -> Iterator[DetectRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start),
                                      end=time_to_duration(end))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                yield DetectRequest(
                    audio=phx_common.Audio(
                        content=data.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                )
                time_range = None
                raw_audio_config = None

    else:
        with open(file, mode="rb") as fd:
            while chunk := fd.read(chunk_size):
                yield DetectRequest(
                    audio=phx_common.Audio(content=chunk, time_range=time_range))
                time_range = None


def print_vad_results(response: DetectResponse, out_file: Optional[pathlib.Path]):
    result = json.dumps(
        MessageToDict(response, always_print_fields_with_no_presence=True,
                      preserving_proto_field_name=True), indent=2)
    if out_file:
        logging.info(f"Writing result to {out_file}")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(result)
    else:
        logging.info("Writing result to stdout")
        print(result)


def get_vad(
        channel: grpc.Channel,
        file: str,
        output_file: Optional[pathlib.Path],
        start: Optional[float],
        end: Optional[float],
        metadata: Optional[list],
        use_raw_audio: bool,
):
    logging.info("Sending audio to Voice Activity Detection microservice")
    stub = VoiceActivityDetectionStub(channel=channel)
    response = stub.Detect(
        make_request(file=file, start=start, end=end, use_raw_audio=use_raw_audio),
        metadata=metadata,
    )
    print_vad_results(response=response, out_file=output_file)


def existing_file(file: str) -> str:
    if not pathlib.Path(file).exists():
        raise argparse.ArgumentError(argument=None,
                                     message=f"File {file} does not exist")
    return file


def main():
    parser = argparse.ArgumentParser(
        description="Voice activity detection gRPC client. Retrieve time sections of audio with voice."
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
        help="Server address, default: localhost:8080",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="error",
        choices=["critical", "error", "warning", "info", "debug"],
    )
    parser.add_argument(
        "--metadata",
        metavar="key=value",
        nargs="+",
        type=lambda x: tuple(x.split("=")),
        help="Custom client metadata",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=None,
        required=False,
        help="Output file with segmentation. If not set, print to standard output.",
    )

    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")
    parser.add_argument("--use_raw_audio", action="store_true", help="Send a raw audio")
    parser.add_argument("file", type=existing_file, help="input audio file")

    args = parser.parse_args()

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")

    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        logging.info(f"Connecting to {args.host}")
        if args.use_ssl:
            with grpc.secure_channel(
                    target=args.host, credentials=grpc.ssl_channel_credentials()
            ) as channel:
                get_vad(
                    channel,
                    args.file,
                    args.output,
                    args.start,
                    args.end,
                    args.metadata,
                    args.use_raw_audio,
                )
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                get_vad(
                    channel,
                    args.file,
                    args.output,
                    args.start,
                    args.end,
                    args.metadata,
                    args.use_raw_audio,
                )

    except grpc.RpcError as e:
        logging.exception(f"RPC failed: {e}")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
