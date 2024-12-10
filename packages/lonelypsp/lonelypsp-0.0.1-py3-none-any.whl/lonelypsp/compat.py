from dataclasses import dataclass as fast_dataclass
import sys
from functools import partial


if sys.version_info >= (3, 10):
    fast_dataclass = partial(fast_dataclass, frozen=True, slots=True)  # type: ignore
else:
    fast_dataclass = partial(fast_dataclass, frozen=True)  # type: ignore
