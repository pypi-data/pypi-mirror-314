import io
from typing import TYPE_CHECKING, Collection, List, Literal, Type, Union

from lonelypsp.sync_io import SyncReadableBytesIO
from lonelypsp.stateful.constants import (
    PubSubStatefulMessageFlags,
    SubscriberToBroadcasterStatefulMessageType,
)
from lonelypsp.stateful.generic_parser import S2B_MessageParser
from lonelypsp.stateful.parser_helpers import parse_simple_headers
from lonelypsp.compat import fast_dataclass
from lonelypsp.stateful.serializer_helpers import (
    MessageSerializer,
    serialize_simple_message,
)


@fast_dataclass
class S2B_Configure:
    """
    S2B = Subscriber to Broadcaster

    See the type enum documentation for more information on the fields
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.CONFIGURE]
    """discriminator value"""

    subscriber_nonce: bytes
    """32 random bytes representing the subscriber's contribution to the nonce"""

    enable_zstd: bool
    """if the client is willing to receive zstandard compressed messages"""

    enable_training: bool
    """if the client may accept custom compression dictionaries"""

    initial_dict: int
    """Either 0 to not recommend an initial preset dictionary, or a positive integer
    representing one of the preset dictionaries that the subscriber believes is appropriate
    for this connection. A value of 1 is ignored.

    Preset dictionaries are typically used when the subscriber may not be connected long
    enough for the cost of training a connection specific dictionary to be properly amortized.
    """


_headers: Collection[str] = ("x-subscriber-nonce", "x-enable-zstd", "x-enable-training")


class S2B_ConfigureParser:
    """Satisfies S2B_MessageParser[S2B_Configure]"""

    @classmethod
    def relevant_types(cls) -> List[SubscriberToBroadcasterStatefulMessageType]:
        return [SubscriberToBroadcasterStatefulMessageType.CONFIGURE]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: SubscriberToBroadcasterStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> S2B_Configure:
        assert type == SubscriberToBroadcasterStatefulMessageType.CONFIGURE

        headers = parse_simple_headers(flags, payload, _headers)
        subscriber_nonce = headers["x-subscriber-nonce"]
        if len(subscriber_nonce) != 32:
            raise ValueError("x-subscriber-nonce must be 32 bytes")

        enable_zstd = headers["x-enable-zstd"] == b"\x01"
        enable_training = headers["x-enable-training"] == b"\x01"

        initial_dict_bytes = headers.get("x-initial-dict", b"0")
        if len(initial_dict_bytes) > 2:
            raise ValueError("x-initial-dict max 2 bytes")

        initial_dict = int.from_bytes(initial_dict_bytes, "big")
        if initial_dict < 0:
            raise ValueError("x-initial-dict must be non-negative")

        return S2B_Configure(
            type=type,
            subscriber_nonce=subscriber_nonce,
            enable_zstd=enable_zstd,
            enable_training=enable_training,
            initial_dict=initial_dict,
        )


if TYPE_CHECKING:
    _: Type[S2B_MessageParser[S2B_Configure]] = S2B_ConfigureParser


def serialize_s2b_configure(
    msg: S2B_Configure, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[S2B_Configure]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_headers,
        header_values=(
            msg.subscriber_nonce,
            b"\x01" if msg.enable_zstd else b"\x00",
            b"\x01" if msg.enable_training else b"\x00",
            msg.initial_dict.to_bytes(2, "big"),
        ),
        payload=b"",
        minimal_headers=minimal_headers,
    )


if TYPE_CHECKING:
    __: MessageSerializer[S2B_Configure] = serialize_s2b_configure
