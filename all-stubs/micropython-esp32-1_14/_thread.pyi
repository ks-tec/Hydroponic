from typing import Any

Node = Any

class LockType:
    def acquire() -> None: ...
    def locked() -> None: ...
    def release() -> None: ...

def allocate_lock() -> None: ...
def exit() -> None: ...
def get_ident() -> None: ...
def stack_size() -> None: ...
def start_new_thread() -> None: ...
