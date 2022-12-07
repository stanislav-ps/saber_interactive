import json
import typing

import argparse
import shutil

from datetime import datetime
from pathlib import Path


_LOG_FILENAME = 'merged_log.jsonl'

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to generate test logs.')

    parser.add_argument(
        dest='path_to_log_a',
        metavar='<PATH/TO/LOG1>',
        type=str,
        help='path to the first input file with generated logs',
    )

    parser.add_argument(
        dest='path_to_log_b',
        metavar='<PATH/TO/LOG2>',
        type=str,
        help='path to second input file with generated logs',
    )

    parser.add_argument(
        '-o',
        dest='path_to_merged_log',
        required=True,
        metavar='<PATH/TO/MERGED/LOG>',
        type=str,
        help='path to the output dir where file with merged logs should be saved',
    )

    parser.add_argument(
        '-f', '--force',
        action='store_const',
        const=True,
        default=False,
        help='force write logs',
        dest='force_write',
    )

    return parser.parse_args()


def log_generator(log_file: Path) -> typing.Generator[dict, None, None]:
    with open(log_file, 'rb') as la_file:

        for line in la_file:
            yield json.loads(line)


def get_next_log(log_from_file_generator: typing.Generator) -> typing.Union[dict, None]:
    try:
        return next(log_from_file_generator)
    except StopIteration:
        return None


def get_log_time(log_instance: dict) -> datetime:
    return datetime.strptime(log_instance.get('timestamp'), DATE_TIME_FORMAT)


def sorted_log_generator(log_a_path: Path, log_b_path: Path) -> typing.Generator[dict, None, None]:
    """
    Compares log entries and generates the one which occurred first."""

    first_file_log_generator = log_generator(log_a_path)
    second_file_log_generator = log_generator(log_b_path)

    first_file_log = get_next_log(first_file_log_generator)
    second_file_log = get_next_log(second_file_log_generator)

    while first_file_log or second_file_log:

        if first_file_log and second_file_log:

            if get_log_time(first_file_log) <= get_log_time(second_file_log):
                yield first_file_log
                first_file_log = get_next_log(first_file_log_generator)

            else:
                yield second_file_log
                second_file_log = get_next_log(second_file_log_generator)

        elif not first_file_log:
            yield second_file_log
            second_file_log = get_next_log(second_file_log_generator)

        elif not second_file_log:
            yield first_file_log
            first_file_log = get_next_log(first_file_log_generator)


def _create_dir(dir_path: Path, *, force_write: bool = False) -> None:
    if dir_path.exists():

        if not force_write:
            raise FileExistsError(
                f'Dir "{dir_path}" already exists. Remove it first or choose another one.')

        shutil.rmtree(dir_path)

    dir_path.mkdir(parents=True)


def main() -> None:
    args = _parse_args()

    log_path_a = Path(args.path_to_log_a)
    log_path_b = Path(args.path_to_log_b)

    if log_path_a.is_file() and log_path_b.is_file():

        merged_log_generator = sorted_log_generator(log_path_a, log_path_b)

        output_dir = Path(args.path_to_merged_log)
        _create_dir(output_dir, force_write=args.force_write)

        output_file_path = output_dir / _LOG_FILENAME

        with output_file_path.open('wb') as file:
            for log_entry in merged_log_generator:
                line = json.dumps(log_entry).encode('utf-8')
                line += b'\n'
                file.write(line)

        print('Done.')

    else:
        raise FileExistsError(
            'Please check the existence of incoming log files and you have specified the correct paths.'
        )


if __name__ == '__main__':
    main()