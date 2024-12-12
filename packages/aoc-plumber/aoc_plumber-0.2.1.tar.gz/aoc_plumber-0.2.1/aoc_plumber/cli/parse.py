from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
import html, re
from .consts import COOKIE_FILE

type Iarg = int | tuple[int, int]


def valid_iarg(value) -> Iarg:
    if value.isdigit():
        return int(value)
    if value == "all":
        return -1
    if (
        "-" in value
        and len(parts := value.split("-")) == 2
        and all(map(str.isdigit, parts))
    ):
        return tuple(map(int, parts))  # type: ignore
    raise ArgumentTypeError(
        f"Invalid value: {value}. Must be a positive integer,"
        " two dash-separated positive integers, or 'all'."
    )


def parse_cmd() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-d", "--day", type=valid_iarg, default=None, help="The day")
    parser.add_argument("-y", "--year", type=valid_iarg, default=None, help="The year")
    parser.add_argument(
        "-c", "--cookie", type=Path, default=COOKIE_FILE, help="The cookie file"
    )
    parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        default=None,
        help="The pattern to use for the folder name",
    )
    parser.add_argument(
        "-m",
        "--match",
        type=str,
        default=None,
        help="Match folder structure and fill days that have no data",
    )
    return parser.parse_args()


def pat_to_regex(pattern):
    escaped_pattern = re.escape(pattern).replace(r"\*", ".*")
    named_regex_pattern = escaped_pattern.replace(
        r"\{year\}", r"(?P<year>\d+)"
    ).replace(r"\{day\}", r"(?P<day>\d+)")
    return re.compile(named_regex_pattern)


def clean_data(data: str) -> str:
    return re.sub(r"<.*?>", "", html.unescape(data.removesuffix("\n")))
