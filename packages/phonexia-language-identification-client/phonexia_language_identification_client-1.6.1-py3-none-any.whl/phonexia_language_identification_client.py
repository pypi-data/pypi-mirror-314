#!/usr/bin/env python3

import argparse
import csv
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Iterator, List, Optional, Tuple

import google.protobuf.duration_pb2
import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.language_identification.v1.language_identification_pb2 as lid
import phonexia.grpc.technologies.language_identification.v1.language_identification_pb2_grpc as lid_grpc
import soundfile
from google.protobuf.json_format import MessageToJson
from phonexia.grpc.common.core_pb2 import RawAudioConfig


# Utility functions
def time_to_duration(time: float) -> Optional[google.protobuf.duration_pb2.Duration]:
    if time is None:
        return None
    duration = google.protobuf.duration_pb2.Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def audio_request_iterator(
    file: Path,
    use_raw_audio: bool,
    request_type: Any,
    time_range: phx_common.TimeRange,
    config: Any,
) -> Iterator:
    if use_raw_audio:
        with soundfile.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )

            for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                logging.debug(f"{data.shape[0]} samples read")
                yield request_type(
                    audio=phx_common.Audio(
                        content=data.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    config=config,
                )
                config = None
                time_range = None
                raw_audio_config = None
    else:
        with open(file, mode="rb") as fd:
            while chunk := fd.read(1024 * 100):  # read by 100kB
                yield request_type(
                    audio=phx_common.Audio(content=chunk, time_range=time_range), config=config
                )
                config = None
                time_range = None


def read_lp(path: Path) -> lid.Languageprint:
    if not path.exists():
        raise ValueError(f"File '{path}' does not exist.")
    with open(path, mode="rb") as file:
        return lid.Languageprint(content=file.read())


def read_adaptation_profile(path: Path) -> lid.AdaptationProfile:
    with open(path, mode="rb") as file:
        return lid.AdaptationProfile(content=file.read())


def write_bin(path: Path, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


# Language Identification
def languageprint_request_iterator(file, config) -> Iterator[lid.IdentifyRequest]:
    yield lid.IdentifyRequest(config=config, languageprint=read_lp(file))


def make_identify_request(
    file: Path,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    languages: Optional[List[lid.Language]],
    groups: Optional[List[lid.LanguageGroup]],
    use_raw_audio: bool,
    adaptation_profile: Optional[Path],
) -> Iterator[lid.IdentifyRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    adaptation_profile = read_adaptation_profile(adaptation_profile) if adaptation_profile else None
    config = lid.IdentifyConfig(
        speech_length=time_to_duration(speech_length),
        languages=languages,
        groups=groups,
        adaptation_profile=adaptation_profile,
    )
    if file.suffix.endswith(("ubj", "lp", "bin")):
        return languageprint_request_iterator(file, config)
    else:
        return audio_request_iterator(file, use_raw_audio, lid.IdentifyRequest, time_range, config)


def write_identification_result(output, response: lid.IdentifyResponse, out_format: str) -> None:
    if out_format == "json":
        output.write(MessageToJson(response))
        return

    langs = {}
    groups = {}
    for res in response.result.scores:
        if len(res.languages) != 0:
            languages = {}
            for lang in res.languages:
                languages[lang.identifier] = lang.probability
            groups[res.identifier] = {"probability": res.probability, "languages": languages}
        else:
            langs[res.identifier] = res.probability

    logging.debug(f"Group probabilities are:\n{groups}")
    logging.debug(f"Language probabilities are:\n{langs}")

    sort_dict = lambda dct: sorted(dct.items(), key=lambda x: x[1], reverse=True)

    logging.info("Writing group probabilities")
    if len(groups) > 0:
        output.write("Group probabilities:\n")
        for identifier, group in groups.items():
            output.write(f"{identifier}\t{group['probability']}\n")
            [output.write(f"\t{lang}\t{prob}\n") for lang, prob in sort_dict(group["languages"])]

    logging.info("Writing language probabilities")
    output.write("Language probabilities:\n")
    [output.write(f"{lang}\t{prob}\n") for lang, prob in sort_dict(langs)]

    output.write(f"Audio length: {response.processed_audio_length.ToJsonString()}\n")
    output.write(f"Speech length: {response.result.speech_length.ToJsonString()}\n")


def identify(
    channel: grpc.Channel,
    input_file: Path,
    output_file: Optional[Path],
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    input_languages: Optional[Path],
    input_groups: Optional[Path],
    metadata: Optional[List],
    out_format: str,
    use_raw_audio: bool,
    adaptation_profile: Optional[Path],
) -> None:
    logging.info("{i} -> {o}".format(i=input_file, o=output_file if output_file else "stdout"))

    logging.debug(f"Parsing input languages {input_languages}")
    languages: Optional[List[lid.Language]] = (
        None
        if input_languages is None
        else [lid.Language(language_code=code) for code in json.loads(input_languages.read_text())]
    )

    logging.debug(f"Parsing input groups {input_groups}")
    groups: Optional[List[lid.LanguageGroup]] = (
        None
        if input_groups is None
        else [
            lid.LanguageGroup(identifier=identifier, language_codes=langs)
            for identifier, langs in json.loads(input_groups.read_text()).items()
        ]
    )

    if input_groups is not None:
        with open(input_groups) as f:
            groups = [
                lid.LanguageGroup(identifier=identifier, language_codes=langs)
                for identifier, langs in json.load(f).items()
            ]

    logging.info(f"Estimating language probabilities from file '{input_file}'")
    stub = lid_grpc.LanguageIdentificationStub(channel)
    response = stub.Identify(
        make_identify_request(
            input_file,
            start,
            end,
            speech_length,
            languages,
            groups,
            use_raw_audio,
            adaptation_profile,
        ),
        metadata=metadata,
    )

    logging.info("Writing results")
    output = open(output_file, "w", encoding="utf8") if output_file else sys.stdout  # noqa: SIM115
    write_identification_result(output, response, out_format)
    if output_file:
        output.close()


# List Supported Languages
def list_supported_languages(
    channel: grpc.Channel,
    output_file: Optional[Path],
    metadata: Optional[List],
    adaptation_profile: Optional[Path],
) -> None:
    logging.info("Getting supported languages")
    adaptation_profile = read_adaptation_profile(adaptation_profile) if adaptation_profile else None
    stub = lid_grpc.LanguageIdentificationStub(channel)
    response: lid.ListSupportedLanguagesResponse = stub.ListSupportedLanguages(
        lid.ListSupportedLanguagesRequest(
            config=lid.ListSupportedLanguagesConfig(adaptation_profile=adaptation_profile)
        ),
        metadata=metadata,
    )

    logging.info("Writing result to {}".format(output_file if output_file else "stdout"))
    output = open(output_file, "w", encoding="utf8") if output_file else sys.stdout  # noqa: SIM115

    output.write("Original languages\n")
    output.write("\n".join(response.supported_languages))
    if len(response.added_languages):
        output.write("\nAdded languages (subset of original languages)\n")
        output.write("\n".join(response.added_languages))
    if len(response.modified_languages):
        output.write("\nModified languages (subset of original languages)\n")
        output.write("\n".join(response.modified_languages))

    if output_file:
        output.close()


# Languageprint Extraction
def make_extract_request(
    file: Path,
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    use_raw_audio: bool,
) -> Iterator[lid.ExtractRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = lid.ExtractConfig(speech_length=time_to_duration(speech_length))
    return audio_request_iterator(file, use_raw_audio, lid.ExtractRequest, time_range, config)


def write_extraction_result(
    audio_path: str, lp_output_file: Path, response: lid.ExtractResponse
) -> None:
    logging.info(f"Writing languageprint to {lp_output_file}")
    write_bin(lp_output_file, response.result.languageprint.content)
    info = {
        "audio": str(audio_path),
        "total_billed_time": str(response.processed_audio_length.ToTimedelta()),
        "speech_length": str(response.result.speech_length.ToTimedelta()),
        "languageprint_file": str(lp_output_file),
    }
    print(json.dumps(info, indent=2))


def extract(
    channel: grpc.Channel,
    input_file: Path,
    output_file: Optional[Path],
    start: Optional[float],
    end: Optional[float],
    speech_length: Optional[float],
    metadata: Optional[List],
    use_raw_audio: bool,
) -> None:
    output_file = output_file or Path(input_file).with_suffix(".ubj")
    logging.info(f"{input_file} -> {output_file}")

    logging.info("Extracting languageprint")
    stub = lid_grpc.LanguageIdentificationStub(channel)

    response = stub.Extract(
        make_extract_request(input_file, start, end, speech_length, use_raw_audio),
        metadata=metadata,
    )

    logging.info("Writing results")
    write_extraction_result(input_file, output_file, response)


# Adaptation profile creation
def make_adapt_request(
    input_list: List[str],
    languages: List[str],
) -> Iterator[lid.AdaptRequest]:
    max_batch_size = 1024
    batch_size = 0
    request = lid.AdaptRequest()
    for [lp_file, language] in zip(input_list, languages):
        logging.debug(f"Appending file '{lp_file}' -> '{language}'.")
        if batch_size >= max_batch_size:
            yield request
            batch_size = 0
            request = lid.AdaptRequest()
        if lp_file:
            lp = read_lp(Path(lp_file))
            unit = lid.AdaptationUnit(
                languageprint=lp, language=lid.Language(language_code=language)
            )
            request.adaptation_units.append(unit)
            batch_size += 1

    if len(request.adaptation_units):
        yield request


def write_adapt_result(output_file: Path, response: lid.AdaptResponse) -> None:
    logging.info(f"Writing adaptation profile to {output_file}")
    write_bin(output_file, response.result.adaptation_profile.content)
    info = {
        "modified_languages": str(response.result.modified_languages),
        "added_languages": str(response.result.added_languages),
        "adaptation_profile_path": str(output_file),
    }
    print(json.dumps(info, indent=2))


def adapt_languages(
    channel: grpc.Channel,
    input_list: List[str],
    languages: List[str],
    output_file: Path,
    metadata: Optional[List],
) -> None:
    logging.info(
        f"Adapting languages using {len(input_list)} languageprints with {len(set(languages))} unique languages."
    )
    logging.info(f"Unique languages are: {set(languages)}.")
    stub = lid_grpc.LanguageIdentificationStub(channel)

    response = stub.Adapt(
        make_adapt_request(input_list, languages),
        metadata=metadata,
    )

    logging.info("Writing results")
    write_adapt_result(output_file, response)


# Main program
def check_file_exists(path: Path) -> Path:
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File '{path}' does not exist.")
    return Path(path)


def parse_list(path: Path, operation: str, identify_ext: str) -> List:
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ", skipinitialspace=True)
        rows = list(reader)

    num_cols = max(len(row) for row in rows)
    if num_cols != min(len(row) for row in rows):
        raise ValueError(f"Two or more rows in '{path}' have different number of columns.")

    if operation == "adapt" and num_cols != 2:
        raise ValueError(
            f"File '{path}' must contain one column with file paths and "
            "one with associated language codes."
        )

    if num_cols < 1 or num_cols > 2:
        raise ValueError(f"File '{path}' must contain one or two columns.")

    if operation == "identify":
        new_extension = f".{identify_ext}"
    elif operation == "extract":
        new_extension = ".ubj"

    def change_extension(path: Path) -> str:
        base = os.path.splitext(path)[0]
        return f"{base}{new_extension}"

    if num_cols == 1:
        for row in rows:
            row.append(change_extension(row[0]))

    return rows


def parse_arguments() -> Tuple[Any, list]:
    parser = argparse.ArgumentParser(
        description=(
            "Language identification gRPC client. Identify language probabilities from an "
            "input audio file."
        ),
    )
    parser.add_argument(
        "operation",
        choices=["identify", "extract", "adapt", "list_languages"],
        help="Select whether to identify languages, extract languageprint, or adapt profile "
        "used for language identification.",
        type=str,
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
        help="Server address, default: localhost:8080",
    )
    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
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
    parser.add_argument("-i", "--input", type=check_file_exists, help="Input audio file")
    parser.add_argument("-o", "--output", type=Path, help="Output file path")
    parser.add_argument(
        "-L",
        "--list",
        type=check_file_exists,
        help="List of files and optional output locations for 'extract' and 'identify' "
        "operations, or files and their appropriate languages for 'adapt' operation.",
    )
    parser.add_argument(
        "-F",
        "--out_format",
        type=str,
        help="Output file format for 'identify' operation",
        default="txt",
        choices=["txt", "json"],
    )
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")
    parser.add_argument("--speech_length", type=float, help="Maximum amount of speech in seconds")
    parser.add_argument("--use_raw_audio", action="store_true", help="Send a raw audio")
    parser.add_argument(
        "--languages",
        type=check_file_exists,
        help="Path to a json file with selected subset of languages for the identification. "
        'The file should contain a json array of language codes, i.e. ["cs-cz", "en-US"]',
    )
    parser.add_argument(
        "--groups",
        type=check_file_exists,
        help="Path to a json file with definitions of groups. The groups must have unique id "
        "and should be assigned disjunct subset of languages. The file should contain a json "
        "dictionary where each key should be a group identifier and value should be a List of "
        'language codes, i.e. {"english": ["en-US", "en-GB"], "arabic": ["ar-IQ", "ar-KW"]}',
    )
    parser.add_argument(
        "--adaptation_profile",
        type=check_file_exists,
        help="Path to a binary file with language adaptation profile used for 'identify' or "
        "'list_languages' operations.",
    )

    return parser.parse_args()


def validate_arguments(args):
    if args.operation == "adapt":
        if args.list is None:
            raise ValueError("Operation 'adapt' must contain 'list' argument.")
        if args.output is None:
            raise ValueError("Operation 'adapt' must contain 'output' argument.")

    if not (args.input or args.list) and args.operation != "list_languages":
        raise ValueError("Either 'input' or 'list' parameter must be set.")

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")

    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.")

    if args.speech_length is not None and args.speech_length < 0:
        raise ValueError("Parameter 'speech_length' must be a non-negative float.")

    if args.output is not None and not os.path.isdir(args.output.parents[0]):
        raise ValueError(f"Output file directory does not exist {args.output}")


def main():
    args = parse_arguments()
    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    validate_arguments(args)

    try:
        logging.info(f"Connecting to {args.host}")
        channel = (
            grpc.secure_channel(target=args.host, credentials=grpc.ssl_channel_credentials())
            if args.use_ssl
            else grpc.insecure_channel(target=args.host)
        )

        if args.operation == "adapt":
            input_files, languages = zip(*parse_list(args.list, args.operation, args.out_format))
            adapt_languages(
                channel,
                input_files,
                languages,
                args.output,
                args.metadata,
            )
        elif args.operation == "list_languages":
            list_supported_languages(channel, args.output, args.metadata, args.adaptation_profile)
        else:

            def execute(input_file: Path, output_file: Path):
                if args.operation == "identify":
                    identify(
                        channel,
                        input_file,
                        output_file,
                        args.start,
                        args.end,
                        args.speech_length,
                        args.languages,
                        args.groups,
                        args.metadata,
                        args.out_format,
                        args.use_raw_audio,
                        args.adaptation_profile,
                    )
                elif args.operation == "extract":
                    extract(
                        channel,
                        input_file,
                        output_file,
                        args.start,
                        args.end,
                        args.speech_length,
                        args.metadata,
                        args.use_raw_audio,
                    )

            if args.input is not None:
                execute(args.input, args.output)

            elif args.list is not None:
                for input_file, output_file in parse_list(
                    args.list, args.operation, args.out_format
                ):
                    execute(Path(input_file), Path(output_file))

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except ValueError as e:
        logging.exception(e)  # noqa: TRY401
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)
    finally:
        channel.close()


if __name__ == "__main__":
    main()
