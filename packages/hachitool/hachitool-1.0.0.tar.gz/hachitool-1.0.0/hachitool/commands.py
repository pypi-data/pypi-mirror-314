import typing as t
import uuid
from contextlib import contextmanager

import pydantic.alias_generators
from pydantic import Field, validate_call, ConfigDict

__all__ = [
    "log",
    "debug",
    "notice",
    "warning",
    "error",
    "fail",
    "mask",
    "log_group",
    "literal",
]


class LogParams(t.TypedDict, total=False):
    __pydantic_config__ = ConfigDict(coerce_numbers_to_str=True)

    title: str
    file: str
    line: int | tuple[int, int]
    column: int | tuple[int, int]


@validate_call(config=ConfigDict(coerce_numbers_to_str=True))
def log(
    level: t.Literal["debug", "notice", "warning", "error"],
    message: str,
    **params: t.Unpack[LogParams],
):
    for key in ["line", "column"]:
        if isinstance(params.get(key), tuple):
            params[key], params[f"end_{key}"] = params[key]

    if params.get("column"):
        params["col"] = params.pop("column")

    param_str = ",".join(
        [f"{pydantic.alias_generators.to_camel(k)}={v}" for k, v in params.items()]
    )

    cmd = level

    if param_str:
        cmd += " " + param_str

    print(f"::{cmd}::{message}")


def debug(message: str, **params):
    log("debug", message, **params)


def notice(message: str, **params):
    log("notice", message, **params)


def warning(message: str, **params):
    log("warning", message, **params)


def error(message: str, **params):
    log("error", message, **params)


def fail(
    message: str = None, /, exit_code: t.Annotated[int, Field(ge=1)] = 1, **params
):
    if message:
        error(message, **params)

    exit(exit_code)


def mask(value: t.Any):
    print(f"::add-mask::{value}")


@contextmanager
@validate_call(config=ConfigDict(coerce_numbers_to_str=True))
def log_group(title: str):
    print(f"::group::{title}")
    yield
    print("::endgroup::")


@contextmanager
def literal():
    signal = uuid.uuid4().hex

    print(f"::stop-commands::{signal}")
    yield
    print(f"::{signal}::")
