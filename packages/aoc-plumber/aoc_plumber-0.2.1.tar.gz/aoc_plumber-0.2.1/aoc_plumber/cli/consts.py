from datetime import datetime
from pathlib import Path

HOME = Path(__file__).parent
DAY = datetime.now().day
YEAR = datetime.now().year
COOKIE_FILE = HOME / "cookie.txt"
