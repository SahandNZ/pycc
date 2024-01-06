import os

from rich.progress import TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn, \
    SpinnerColumn, MofNCompleteColumn

# Directories
HOME_DIR = os.path.expanduser('~')
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(HOME_DIR, "Data"))

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
