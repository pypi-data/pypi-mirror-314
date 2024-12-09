import sys
import time
from enum import Enum
from datetime import datetime

class LogTypes(Enum):
    ERR = "[ERROR]"
    INFO = "[INFO]"
    SUCCESS = "[SUCCESS]"
    WARN = "[WARNING]"

def typewrite(*values: object, interval: float = 0.1):
    """
    Creates a typewriting effect and optionally scrolls long text by printing it line by line.

    ## Parameters:
    *values (object): Objects to be printed.
    interval (float): Time delay between each character. Default is 0.1 seconds.
    """
    text = " ".join(map(str, values))
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(interval)
    print()

def log(type: LogTypes, log: str, timestamp: bool = False):
    """
    Logs information.

    ## Parameters
    type (LogTypes): The type of log.
    log (str): The message to log.
    timestamp (bool): Wether or not to include the timestamp of the log. 
    """
    timestamp_str = ""
    if timestamp:
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S") + " "
    print(f"{timestamp_str}{type.value} {log}")

def blink_text(text: str, duration: int, interval: float) -> None:
    """
    Creates blinking text.

    ## Parameters:
    text (str): The text to flash.
    duration (int): The number of seconds to flash.
    interval (float): The interval in seconds between flashes.
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        print(text, end="\r", flush=True)
        time.sleep(interval)
        print(" " * len(text), end="\r", flush=True)
        time.sleep(interval)

def progress_bar(iterable, total: int, progress_interval: float = 0.1):
    """
    Displays a progress bar in the terminal while iterating over an iterable.

    ## Parameters:
    - iterable (iterable): The iterable (e.g., list, range, etc.) over which to iterate.
    - total (int): The total number of items in the iterable, used to calculate the progress percentage.
    - progress_interval (float, optional): The time interval (in seconds) between updates of the progress bar.
      Defaults to 0.1 seconds.
    """
    for i, _ in enumerate(iterable, 1):
        percent = int(i / total * 100)
        bar = '#' * (percent // 2)
        sys.stdout.write(f"\r[{bar:<50}] {percent}%")
        sys.stdout.flush()
        time.sleep(progress_interval)
    sys.stdout.write("\n")
