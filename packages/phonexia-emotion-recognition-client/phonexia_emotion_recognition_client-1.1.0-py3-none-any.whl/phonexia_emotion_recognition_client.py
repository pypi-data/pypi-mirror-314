import argparse
import json
import logging
import pathlib
from typing import Iterator, Optional

import grpc
from google.protobuf.duration_pb2 import Duration
from phonexia.grpc.common.core_pb2 import Audio, RawAudioConfig, TimeRange
from phonexia.grpc.technologies.emotion_recognition.v1.emotion_recognition_pb2 import (
    EmotionScore,
    RecognizeConfig,
    RecognizeRequest,
    RecognizeResponse,
)
from phonexia.grpc.technologies.emotion_recognition.v1.emotion_recognition_pb2_grpc import (
    EmotionRecognitionStub,
)
from soundfile import SoundFile


def time_to_duration(time: float) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
    file: str,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    use_raw_audio: bool,
) -> Iterator[RecognizeRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = RecognizeConfig(speech_length=time_to_duration(speech_length))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                yield RecognizeRequest(
                    audio=Audio(
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
                yield RecognizeRequest(
                    audio=Audio(content=chunk, time_range=time_range), config=config
                )
                time_range = None


def write_result(
    audio_path: str, response: RecognizeResponse, output_file: Optional[str] = None
) -> None:
    output_file = output_file or str(pathlib.Path(audio_path).with_suffix(".json"))
    result = {
        "total_billed_time": str(response.processed_audio_length.ToTimedelta()),
        "speech_length": str(response.result.speech_length.ToTimedelta()),
        "emotions": {},
    }
    for score in response.result.scores:
        result["emotions"][EmotionScore.EmotionType.Name(score.emotion)] = float(score.probability)

    logging.debug(f"Result of the recognition is {result}")

    logging.info(f"Writing results of the recognition to '{output_file}'")
    with open(output_file, "w") as f:
        f.write(json.dumps(result, indent=2))


def recognize(
    channel: grpc.Channel,
    file: str,
    output_file: Optional[str],
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
) -> None:
    logging.info(f"Detecting emotions from '{file}'")
    stub = EmotionRecognitionStub(channel)
    response = stub.Recognize(
        make_request(file, start, end, speech_length, use_raw_audio),
        metadata=metadata,
    )
    write_result(file, response, output_file)


def existing_file(file: str) -> str:
    if not pathlib.Path(file).exists():
        raise argparse.ArgumentError(argument=None, message=f"File {file} does not exist")
    return file


def main():
    parser = argparse.ArgumentParser(
        description="Emotion recognition gRPC client. Recognize possible presence of emotions from audio with voice."
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
    parser.add_argument("--speech_length", type=float, help="Maximum amount of speech in seconds")
    parser.add_argument("--use_raw_audio", action="store_true", help="Send a raw audio")
    parser.add_argument("file", type=existing_file, help="input audio file")

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

    try:
        logging.info(f"Connecting to {args.host}")
        if args.use_ssl:
            with grpc.secure_channel(
                target=args.host, credentials=grpc.ssl_channel_credentials()
            ) as channel:
                recognize(
                    channel=channel,
                    file=args.file,
                    output_file=args.output,
                    start=args.start,
                    end=args.end,
                    speech_length=args.speech_length,
                    metadata=args.metadata,
                    use_raw_audio=args.use_raw_audio,
                )
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                recognize(
                    channel=channel,
                    file=args.file,
                    output_file=args.output,
                    start=args.start,
                    end=args.end,
                    speech_length=args.speech_length,
                    metadata=args.metadata,
                    use_raw_audio=args.use_raw_audio,
                )

    except grpc.RpcError as e:
        logging.exception(f"RPC failed: {e}")  # noqa: TRY401
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
