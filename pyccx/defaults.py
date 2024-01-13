import os

from rich.progress import TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn, \
    SpinnerColumn, MofNCompleteColumn

# Directories
HOME_DIR = os.path.expanduser('~')
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(HOME_DIR, "Data"))
CANDLE_DIR = os.path.join(DATA_DIR, "candle")

# proxies
HTTP_PROXY = os.environ.get("PYCCX_HTTP_PROXY", None)
HTTPS_PROXY = os.environ.get("PYCCX_HTTPS_PROXY", None)
SOCKS5_PROXY = os.environ.get("PYCCX_SOCKS_PROXY", None)
PROXIES = {"http": HTTP_PROXY, "https": HTTPS_PROXY, "socks5": SOCKS5_PROXY}

# Properties
BASE_TIME_FRAME = os.environ.get("BASE_TIME_FRAME", 900)

# Rich progress bar columns
RICH_PROGRESS_COLUMNS = [
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(show_speed=True),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
]
