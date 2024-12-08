import os
import typing as t
from enum import StrEnum
from pathlib import Path
from types import SimpleNamespace

from multimethod import multimethod
from pydantic import ConfigDict, validate_call

__all__ = ["set_output", "set_env", "add_path", "summary"]


class File(StrEnum):
    OUTPUT = "OUTPUT"
    ENV = "ENV"
    PATH = "PATH"
    SUMMARY = "STEP_SUMMARY"

    @property
    def file(self):
        return Path(os.getenv(f"GITHUB_{self.value}"))

    @validate_call(config=ConfigDict(coerce_numbers_to_str=True))
    def write(self, content: str, append: bool = True):
        print(content, file=self.file.open("a" if append else "w"))


@multimethod
def _write_kv(file: File, key: t.Any, value: t.Any):
    file.write(f"{key}={value}")


@multimethod
def _write_kv(file: File, data: dict):
    for key, value in data.items():
        _write_kv(file, key, value)


@multimethod
def _write_kv(file: File, **kwargs):
    _write_kv(file, kwargs)


def set_output(*args, **kwargs):
    _write_kv(File.OUTPUT, *args, **kwargs)


def set_env(*args, **kwargs):
    _write_kv(File.ENV, *args, **kwargs)


@validate_call
def add_path(path: Path):
    File.PATH.write(str(path))


class Summary(SimpleNamespace):
    @staticmethod
    def add(content: str, /, overwrite: bool = False):
        File.SUMMARY.write(content, append=not overwrite)

    @staticmethod
    def clear():
        File.SUMMARY.file.unlink(missing_ok=True)

    __call__ = add


summary = Summary
