from pathlib import Path
import os, requests
from glob import glob
from textwrap import dedent

from .parse import Iarg, parse_cmd, pat_to_regex, clean_data
from .consts import COOKIE_FILE, YEAR, DAY, HOME


def download_day(day: int, year: int, cookie: str, pattern: str = "Day_{day}") -> None:
    folder = Path(pattern.format(day=day, year=year))
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
    response = requests.get(url, cookies={"session": cookie})

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


def main():
    args = parse_cmd()

    if not args.cookie.exists():
        print(
            f"Please create a cookie.txt file in the same directory as this script ({COOKIE_FILE})."
        )
        exit()

    COOKIE = args.cookie.read_text().strip()

    year: Iarg = args.year if args.year is not None else YEAR
    day: Iarg = args.day if args.day is not None else DAY
    PATTERN: str = args.pattern or ("{year}/Day_{day}" if year != YEAR else "Day_{day}")

    # If match, ignore all else
    if args.match is not None:
        glob_pattern = args.match.replace("{day}", "*").replace("{year}", "*")
        compiled_pattern = pat_to_regex(args.match)
        for folder in glob(glob_pattern, root_dir=HOME):
            if match := compiled_pattern.match(folder):
                dct = match.groupdict()
                year = int(dct.get("year", YEAR))
                day = int(dct.get("day", DAY))
                download_day(day, year, COOKIE, pattern=folder)
                print(f"Downloaded Day {day} of {year}")
        exit()

    def to_list(
        value: int | tuple[int, int], default: list[int], name: str
    ) -> list[int]:
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
            download_day(day, year, COOKIE, pattern=PATTERN)
            print(f"Downloaded Day {day} of {year}")
