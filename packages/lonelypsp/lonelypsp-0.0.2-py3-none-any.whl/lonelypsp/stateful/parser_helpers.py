from types import TracebackType
from typing import Dict, Generator, Generic, Iterable, Iterator, List, Type, TypeVar
from lonelypsp.sync_io import SyncReadableBytesIO
from lonelypsp.compat import fast_dataclass
from lonelypsp.stateful.constants import (
    BroadcasterToSubscriberStatefulMessageType,
    PubSubStatefulMessageFlags,
    SubscriberToBroadcasterStatefulMessageType,
)


@fast_dataclass
class B2S_MessagePrefix:
    """
    B2S = Broadcaster to subscriber

    Describes the first 4 bytes of the message that are common to all B2S messages
    which are required to know how to parse the rest of the message
    """

    flags: PubSubStatefulMessageFlags
    """bit flags for parsing the message"""

    type: BroadcasterToSubscriberStatefulMessageType
    """enum value describing the contents of the message"""


def parse_b2s_message_prefix(body: SyncReadableBytesIO) -> B2S_MessagePrefix:
    """Consumes and interprets the first four bytes of a broadcaster to
    subscriber message. This is 2 bytes for flags and then 2 bytes for the
    message type discriminator.

    Raises ValueError if the message is too short to contain the prefix
    or is otherwise malformed

    Propagates errors from reading the body
    """
    flags_bytes = read_exact(body, 2)
    flags_int = int.from_bytes(flags_bytes, "big")
    flags = PubSubStatefulMessageFlags(flags_int)

    message_type_bytes = read_exact(body, 2)
    message_type_int = int.from_bytes(message_type_bytes, "big")
    message_type = BroadcasterToSubscriberStatefulMessageType(message_type_int)

    return B2S_MessagePrefix(flags, message_type)


@fast_dataclass
class S2B_MessagePrefix:
    """
    S2B = Subscriber to Broadcaster

    Describes the first 4 bytes of the message that are common to all S2B messages
    which are required to know how to parse the rest of the message
    """

    flags: PubSubStatefulMessageFlags
    """bit flags for parsing the message"""

    type: SubscriberToBroadcasterStatefulMessageType
    """enum value describing the contents of the message"""


def parse_s2b_message_prefix(body: SyncReadableBytesIO) -> S2B_MessagePrefix:
    """Consumes and interprets the first four bytes of a subscriber to
    broadcaster message. This is 2 bytes for flags and then 2 bytes for the
    message type discriminator.

    Raises ValueError if the message is too short to contain the prefix
    or is otherwise malformed

    Propagates errors from reading the body
    """
    flags_bytes = read_exact(body, 2)
    flags_int = int.from_bytes(flags_bytes, "big")
    flags = PubSubStatefulMessageFlags(flags_int)

    message_type_bytes = read_exact(body, 2)
    message_type_int = int.from_bytes(message_type_bytes, "big")
    message_type = SubscriberToBroadcasterStatefulMessageType(message_type_int)

    return S2B_MessagePrefix(flags, message_type)


T = TypeVar("T")


class GeneratorContextManager(Generic[T]):
    """Convenience class which makes working with generators easier by
    acting as a context manager that automatically closes the generator
    and provides the iterator
    """

    def __init__(self, gen: Generator[T, None, None]) -> None:
        self.gen = gen

    def __enter__(self) -> Iterator[T]:
        return self.gen.__iter__()

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.gen.close()


def read_exact(stream: SyncReadableBytesIO, n: int) -> bytes:
    """Reads exactly the indicated number of bytes, raising an exception if
    the stream ends before the bytes are read
    """
    data = stream.read(n)
    if len(data) != n:
        raise ValueError(f"underflow: expected {n} bytes, got {len(data)}")
    return data


def parse_minimal_message_headers(
    body: SyncReadableBytesIO,
) -> Generator[bytes, None, None]:
    """Consumes and parses minimal headers from the body, yielding
    after each one. Should be interrupted once all headers have been
    read. This is parsing the following format, where N is some value
    that the caller can determine

    - Repeat N:
        - 2 bytes (L): length of header value, big-endian encoded, unsigned
        - L bytes: header value

    Raises ValueError if the headers are malformed

    Propagates errors from reading the body
    """

    while True:
        header_length_bytes = read_exact(body, 2)
        header_length = int.from_bytes(header_length_bytes, "big")
        header_value = read_exact(body, header_length)
        yield header_value


def parse_expanded_headers(body: SyncReadableBytesIO) -> Dict[str, bytes]:
    """Parses the expanded headers at the given position in the body,
    returning a dictionary of header names to header values. The header
    names are ascii and lowercase, so they are unambiguous. When a header
    is repeated, the last value is used.

    - 2 bytes (N): number of headers, big-endian encoded, unsigned
    - REPEAT N:
        - 2 bytes (M): length of header name, big-endian encoded, unsigned
        - M bytes: header name, ascii-encoded
        - 2 bytes (L): length of header value, big-endian encoded, unsigned
        - L bytes: header value

    Raises ValueError if the headers are malformed

    Propagates errors from reading the body
    """
    header_count_bytes = read_exact(body, 2)
    header_count = int.from_bytes(header_count_bytes, "big")

    headers: Dict[str, bytes] = {}
    for _ in range(header_count):
        header_name_length_bytes = read_exact(body, 2)
        header_name_length = int.from_bytes(header_name_length_bytes, "big")
        header_name = read_exact(body, header_name_length).decode("ascii").lower()

        header_value_length_bytes = read_exact(body, 2)
        header_value_length = int.from_bytes(header_value_length_bytes, "big")
        header_value = read_exact(body, header_value_length)

        headers[header_name] = header_value

    return headers


def parse_simple_headers(
    flags: PubSubStatefulMessageFlags,
    body: SyncReadableBytesIO,
    minimal_headers: Iterable[str],
) -> Dict[str, bytes]:
    """Consumes and parses headers from the body, returning a dictionary
    of header names to header values. The header names are ascii and lowercase,
    so they are unambiguous. When a header is repeated, the last value is used.

    When minimal headers are provided, assumes they are exactly those specified in
    the list. If the headers are malformed, raises ValueError.

    Propagates errors from reading the body
    """
    if (flags & PubSubStatefulMessageFlags.MINIMAL_HEADERS) != 0:
        result: Dict[str, bytes] = {}
        with GeneratorContextManager(parse_minimal_message_headers(body)) as parser:
            for name in minimal_headers:
                result[name] = next(parser)
        return result

    return parse_expanded_headers(body)
