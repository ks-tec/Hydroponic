from token import *
from typing import Any

COMMENT: Any
NL: Any
ENCODING: Any

class TokenInfo:
    def __str__(self): ...

def get_indent(l): ...
def get_str(l, readline): ...
def tokenize(readline) -> None: ...
