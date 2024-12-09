import typing as t

def log(
    level: t.Literal["debug", "notice", "warning", "error"],
    message: str,
    /,
    title: str = None,
    file: str = None,
    line: int | tuple[int, int] = None,
    column: int | tuple[int, int] = None,
): ...
def debug(
    message: str,
    /,
    title: str = None,
    file: str = None,
    line: int | tuple[int, int] = None,
    column: int | tuple[int, int] = None,
): ...
def notice(
    message: str,
    /,
    title: str = None,
    file: str = None,
    line: int | tuple[int, int] = None,
    column: int | tuple[int, int] = None,
): ...
def warning(
    message: str,
    /,
    title: str = None,
    file: str = None,
    line: int | tuple[int, int] = None,
    column: int | tuple[int, int] = None,
): ...
def error(
    message: str,
    /,
    title: str = None,
    file: str = None,
    line: int | tuple[int, int] = None,
    column: int | tuple[int, int] = None,
): ...
def fail(
    message: str,
    /,
    exit_code: int = 1,
    title: str = None,
    file: str = None,
    line: int | tuple[int, int] = None,
    column: int | tuple[int, int] = None,
): ...
def mask(value: str): ...
def log_group(title: str): ...
def literal(): ...
