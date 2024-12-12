from dataclasses import dataclass as fast_dataclass
import sys
from functools import partial
from typing import TypeVar

T = TypeVar("T")

if sys.version_info >= (3, 10):

    def make_dataclass_fast(x: T) -> T:
        return partial(x, frozen=True, slots=True)  # type: ignore

    fast_dataclass = make_dataclass_fast(fast_dataclass)
else:

    def make_dataclass_fast(x: T) -> T:
        return partial(x, frozen=True)  # type: ignore

    fast_dataclass = make_dataclass_fast(fast_dataclass)
