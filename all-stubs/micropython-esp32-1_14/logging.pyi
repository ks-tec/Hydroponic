from typing import Any

Node = Any

class Logger:
    def _level_str() -> None: ...
    def critical() -> None: ...
    def debug() -> None: ...
    def error() -> None: ...
    def exc() -> None: ...
    def exception() -> None: ...
    def info() -> None: ...
    def isEnabledFor() -> None: ...
    def log() -> None: ...
    def setLevel() -> None: ...
    def warning() -> None: ...

def basicConfig() -> None: ...
def debug() -> None: ...
def getLogger() -> None: ...
def info() -> None: ...
