from typing import TYPE_CHECKING, Protocol, Type, Union


class SyncReadableBytesIOA(Protocol):
    """A type that represents a stream that can be read synchronously"""

    def read(self, n: int) -> bytes:
        """Reads n bytes from the file-like object"""
        raise NotImplementedError()


class SyncReadableBytesIOB(Protocol):
    """A type that represents a stream that can be read synchronously"""

    def read(self, n: int, /) -> bytes:
        """Reads n bytes from the file-like object"""
        raise NotImplementedError()


SyncReadableBytesIO = Union[SyncReadableBytesIOA, SyncReadableBytesIOB]


class SyncWritableBytesIO(Protocol):
    """A type that represents a stream that can be written synchronously"""

    def write(self, b: Union[bytes, bytearray], /) -> int:
        """Writes the given bytes to the file-like object"""
        raise NotImplementedError()


class Closeable(Protocol):
    """Represents something that can be closed"""

    def close(self) -> None:
        """Closes the file-like object"""


class SyncTellableBytesIO(Protocol):
    """A type that represents a stream with a synchronous tell method"""

    def tell(self) -> int:
        """Returns the current position in the file"""
        raise NotImplementedError()


class SyncSeekableBytesIO(Protocol):
    """A type that represents a stream with a synchronous seek method"""

    def seek(self, offset: int, whence: int = 0) -> int:
        """Seeks to a position in the file"""
        raise NotImplementedError()


class SyncStandardIOA(
    SyncReadableBytesIOA, SyncTellableBytesIO, SyncSeekableBytesIO, Protocol
): ...


class SyncStandardIOB(
    SyncReadableBytesIOA, SyncTellableBytesIO, SyncSeekableBytesIO, Protocol
): ...


SyncStandardIO = Union[SyncStandardIOA, SyncStandardIOB]


class PreallocatedBytesIO:
    """Convenience object that acts like BytesIO, but you can specify the length
    in advance
    """

    def __init__(self, length: int) -> None:
        self.buffer = bytearray(length)
        self.pos = 0

    def read(self, n: int) -> bytes:
        if n < 0:
            n = len(self.buffer) - self.pos

        result = self.buffer[self.pos : self.pos + n]
        self.pos = min(self.pos + n, len(self.buffer))
        return result

    def write(self, b: Union[bytes, bytearray], /) -> int:
        end_index = self.pos + len(b)
        if end_index > len(self.buffer):
            raise ValueError("writing past the end of the buffer")

        self.buffer[self.pos : end_index] = b
        self.pos = end_index

        return len(b)

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = 0) -> int:
        if whence == 0:
            self.pos = offset
        elif whence == 1:
            self.pos += offset
        elif whence == 2:
            self.pos = len(self.buffer) + offset
        else:
            raise ValueError("invalid whence value")

        if self.pos < 0:
            self.pos = 0
        elif self.pos > len(self.buffer):
            self.pos = len(self.buffer)
        return self.pos

    def close(self) -> None:
        pass


if TYPE_CHECKING:
    _: Type[SyncStandardIO] = PreallocatedBytesIO
