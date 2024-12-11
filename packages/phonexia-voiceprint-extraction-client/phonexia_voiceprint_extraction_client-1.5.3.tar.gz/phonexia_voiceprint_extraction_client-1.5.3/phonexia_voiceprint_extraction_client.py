#!/usr/bin/env python3

import argparse
import json
import logging
import os
import pathlib
from typing import Iterator, Optional

import google.protobuf.duration_pb2
import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2 as sid
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2_grpc as sid_grpc
import soundfile
from phonexia.grpc.common.core_pb2 import RawAudioConfig


def time_to_duration(time: float) -> Optional[google.protobuf.duration_pb2.Duration]:
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
    speech_length: Optional[float],
    use_raw_audio: bool,
) -> Iterator[sid.ExtractRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = sid.ExtractConfig(speech_length=time_to_duration(speech_length))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                yield sid.ExtractRequest(
                    audio=phx_common.Audio(
                        content=data.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    config=config,
                )
                time_range = None
                raw_audio_config = None

    else:
        with open(file, mode="rb") as fd:
            while chunk := fd.read(chunk_size):
                yield sid.ExtractRequest(
                    audio=phx_common.Audio(content=chunk, time_range=time_range), config=config
                )
                time_range = None


def voiceprint_path(audio_path: str) -> str:
    suffix = ".ubj"
    return str(pathlib.Path(audio_path).with_suffix(suffix))


def write_voiceprint(path: str, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


def write_result(
    audio_path: str, response: sid.ExtractResponse, vp_output_file: Optional[str] = None
) -> None:
    vp_path = vp_output_file or voiceprint_path(audio_path)
    logging.info(f"Writing voiceprint to {vp_path}")
    write_voiceprint(vp_path, response.result.voiceprint.content)
    info = {
        "audio": audio_path,
        "total_billed_time": str(response.processed_audio_length.ToTimedelta()),
        "speech_length": str(response.result.speech_length.ToTimedelta()),
        "voiceprint_file": vp_path,
    }
    print(json.dumps(info, indent=2))


def extract_vp(
    channel: grpc.Channel,
    file: str,
    vp_output_file: Optional[str],
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
) -> None:
    logging.info(f"Extracting voiceprints from {file}")
    stub = sid_grpc.VoiceprintExtractionStub(channel)
    response = stub.Extract(
        make_request(file, start, end, speech_length, use_raw_audio),
        metadata=metadata,
    )
    write_result(file, response, vp_output_file)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Voiceprint extraction gRPC client. Extracts voiceprint from an input audio file."
        ),
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
        type=str,
        default=None,
        required=False,
        help="Output ubjson voiceprint file",
    )
    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")
    parser.add_argument("--speech_length", type=float, help="Maximum amount of speech in seconds")
    parser.add_argument("--use_raw_audio", action="store_true", help="Send a raw audio")
    parser.add_argument("file", type=str, help="input audio file")

    args = parser.parse_args()

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")

    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.")

    if args.speech_length is not None and args.speech_length <= 0:
        raise ValueError("Parameter 'speech_length' must be float larger than 0.")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not os.path.isfile(args.file):
        logging.error(f"no such file {args.file}")
        exit(1)

    try:
        logging.info(f"Connecting to {args.host}")
        if args.use_ssl:
            with grpc.secure_channel(
                target=args.host, credentials=grpc.ssl_channel_credentials()
            ) as channel:
                extract_vp(
                    channel,
                    args.file,
                    args.output,
                    args.start,
                    args.end,
                    args.speech_length,
                    args.metadata,
                    args.use_raw_audio,
                )
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                extract_vp(
                    channel,
                    args.file,
                    args.output,
                    args.start,
                    args.end,
                    args.speech_length,
                    args.metadata,
                    args.use_raw_audio,
                )

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
