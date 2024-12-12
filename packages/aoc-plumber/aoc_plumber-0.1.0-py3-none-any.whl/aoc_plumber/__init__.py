import html, os, re, requests
from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from glob import glob
from pathlib import Path
from textwrap import dedent


HOME = Path(__file__).parent
COOKIE_FILE = HOME / "cookie.txt"
DAY = datetime.now().day
YEAR = datetime.now().year


def valid_iarg(value) -> int | tuple[int, int]:
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


parser = ArgumentParser()
parser.add_argument("-d", "--day", type=valid_iarg, default=DAY, help="The day")
parser.add_argument("-y", "--year", type=valid_iarg, default=YEAR, help="The year")
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
args = parser.parse_args()

if not args.cookie.exists():
    print(f"Please create a cookie.txt file in the same directory as this script ({COOKIE_FILE}).")
    exit()
COOKIE = args.cookie.read_text().strip()

year: int | tuple[int, int] = args.year
day: int | tuple[int, int] = args.day
PATTERN: str = args.pattern or ("{year}/Day_{day}" if year != YEAR else "Day_{day}")


def pat_to_regex(pattern):
    escaped_pattern = re.escape(pattern).replace(r"\*", ".*")
    named_regex_pattern = escaped_pattern.replace(
        r"\{year\}", r"(?P<year>\d+)"
    ).replace(r"\{day\}", r"(?P<day>\d+)")
    return re.compile(named_regex_pattern)


def clean_data(data: str) -> str:
    return re.sub(r"<.*?>", "", html.unescape(data.removesuffix("\n")))


def download_day(day: int, year: int, pattern: str = "Day_{day}") -> None:
    folder = HOME / pattern.format(day=day, year=year)
    os.makedirs(folder, exist_ok=True)

    url = f"https://adventofcode.com/{year}/day/{day}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        if not (folder / "test.txt").exists():
            (folder / "test.txt").write_text(
                clean_data(data.split("<pre><code>")[1].split("</code></pre>")[0])
            )
    else:
        print(f"Failed to download data from {url}")

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": COOKIE})

    if response.status_code == 200:
        if not (folder / "input.txt").exists():
            (folder / "input.txt").write_text(response.text.rstrip())
    else:
        print(f"Failed to download data from {url}")

    template = dedent(
        """\
    from pathlib import Path

    HOME = Path(__file__).parent

    with open(HOME/"test.txt") as f:
        pass
    """
    )

    for part in range(1, 3):
        path = folder / f"p{part}.py"
        if not path.exists():
            path.write_text(template)


# If match, ignore all else
if args.match is not None:
    glob_pattern = args.match.replace("{day}", "*").replace("{year}", "*")
    compiled_pattern = pat_to_regex(args.match)
    for folder in glob(glob_pattern, root_dir=HOME):
        if match := compiled_pattern.match(folder):
            dct = match.groupdict()
            year = int(dct.get("year", YEAR))
            day = int(dct.get("day", DAY))
            download_day(day, year, pattern=folder)
            print(f"Downloaded Day {day} of {year}")
    exit()


def to_list(value: int | tuple[int, int], default: list[int], name: str) -> list[int]:
    if isinstance(value, tuple):
        s, e = value
        if s > e:
            print(f"Invalid {name} range {s}-{e}")
            exit()
        return list(range(s, e + 1))
    return default if value == -1 else [value]


years = to_list(year, list(range(2015, YEAR + 1)), "year")
days = to_list(day, list(range(1, max(26, DAY + 1))), "day")

for year in years:
    for day in days:
        if year == YEAR and day > DAY:
            print(f"Day {day} of {year} has not arrived yet.")
            break
        download_day(day, year, pattern=PATTERN)
        print(f"Downloaded Day {day} of {year}")
