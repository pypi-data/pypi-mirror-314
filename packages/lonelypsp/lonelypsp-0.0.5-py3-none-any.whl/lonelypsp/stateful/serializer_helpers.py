from typing import Collection, Generic, Protocol, TypeVar, Union
from lonelypsp.sync_io import PreallocatedBytesIO, SyncWritableBytesIO
from lonelypsp.stateful.constants import (
    BroadcasterToSubscriberStatefulMessageType,
    PubSubStatefulMessageFlags,
    SubscriberToBroadcasterStatefulMessageType,
)


def serialize_prefix(
    out: SyncWritableBytesIO,
    type: Union[
        SubscriberToBroadcasterStatefulMessageType,
        BroadcasterToSubscriberStatefulMessageType,
    ],
    /,
    *,
    minimal_headers: bool,
) -> None:
    """Writes the message flags and the type of message to the output stream."""
    out.write(
        int.to_bytes(
            PubSubStatefulMessageFlags.MINIMAL_HEADERS if minimal_headers else 0,
            2,
            "big",
        )
    )
    out.write(int.to_bytes(type, 2, "big"))


def serialize_minimal_headers(
    out: SyncWritableBytesIO, values: Collection[bytes]
) -> None:
    """Writes the header values to the output stream, in minimal headers mode.

    Minimal headers does not get prefixed with the number of headers and the
    name of the headers is implicit from their order, thus this can be called
    multiple times to write multiple headers.
    """
    for value in values:
        out.write(int.to_bytes(len(value), 2, "big"))
        out.write(value)


def serialize_expanded_headers(
    out: SyncWritableBytesIO,
    header_names: Collection[str],
    header_values: Collection[bytes],
    /,
) -> None:
    """Writes the header values to the output stream, in expanded headers mode.

    Expanded headers get prefixed with the number of headers and the name of
    the headers, thus this can be called only once to write all headers.
    """
    assert len(header_names) == len(header_values)
    out.write(int.to_bytes(len(header_names), 2, "big"))
    for name, value in zip(header_names, header_values):
        out.write(int.to_bytes(len(name), 2, "big"))
        out.write(name.encode("ascii"))
        out.write(int.to_bytes(len(value), 2, "big"))
        out.write(value)


def serialize_simple_headers(
    out: SyncWritableBytesIO,
    header_names: Collection[str],
    header_values: Collection[bytes],
    /,
    *,
    minimal: bool,
) -> None:
    """Writes the given headers for the contents of a websocket message
    to the output stream in the appropriate mode.
    """

    if minimal:
        serialize_minimal_headers(out, header_values)
    else:
        serialize_expanded_headers(out, header_names, header_values)


def serialize_simple_message(
    *,
    type: Union[
        SubscriberToBroadcasterStatefulMessageType,
        BroadcasterToSubscriberStatefulMessageType,
    ],
    header_names: Collection[str],
    header_values: Collection[bytes],
    payload: bytes,
    minimal_headers: bool,
) -> Union[bytes, bytearray, memoryview]:
    """Serializes the entire contents of a websocket message with the given
    type, headers, and payload, returning the bytes contents to send along
    the websocket
    """
    assert len(header_names) == len(header_values)
    total_size = (
        2  # flags
        + 2  # type
        + (  # headers
            2 * len(header_values) + sum(len(value) for value in header_values)
            if minimal_headers
            else 2
            + 4 * len(header_values)
            + sum(len(name.encode("ascii")) for name in header_names)
            + sum(len(value) for value in header_values)
        )
        + len(payload)
    )

    out = PreallocatedBytesIO(total_size)
    serialize_prefix(out, type, minimal_headers=minimal_headers)
    serialize_simple_headers(out, header_names, header_values, minimal=minimal_headers)
    out.write(payload)
    assert out.tell() == total_size
    return out.buffer


def int_to_minimal_unsigned(n: int) -> bytes:
    """Converts an integer to a minimal unsigned byte representation. In order
    to parse this the parser will need to know the length in bytes from the protocol,
    e.g., because it's a header value.

    Result is big-endian encoded
    """
    assert n >= 0
    bit_length = (n.bit_length() - 1) // 8 + 1
    return n.to_bytes(bit_length, "big")


T_contra = TypeVar("T_contra", contravariant=True)


class MessageSerializer(Generic[T_contra], Protocol):
    """The protocol the serializer functions should satisfy, to ensure we
    are being consistent
    """

    def __call__(
        self, msg: T_contra, /, *, minimal_headers: bool
    ) -> Union[bytes, bytearray, memoryview]:
        """Serializes the given message into the bytes to send within a websocket
        bytes message.

        Args:
            msg: The message to serialize
            minimal_headers: True to use minimal headers, False to use expanded headers.
                Generally this is configured individually by broadcasters and subscribers,
                and only turned off as part of the process of updating the protocol before
                being turned back on when everything is on the same version.
        """
