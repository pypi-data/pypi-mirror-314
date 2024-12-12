import hashlib
from typing import TYPE_CHECKING, Collection, List, Literal, Optional, Type, Union

from lonelypsp.sync_io import SyncReadableBytesIO
from lonelypsp.stateful.constants import (
    PubSubStatefulMessageFlags,
    SubscriberToBroadcasterStatefulMessageType,
)
from lonelypsp.compat import fast_dataclass
from lonelypsp.stateful.generic_parser import S2B_MessageParser
from lonelypsp.stateful.parser_helpers import parse_simple_headers
from lonelypsp.stateful.serializer_helpers import (
    MessageSerializer,
    int_to_minimal_unsigned,
    serialize_simple_message,
)


@fast_dataclass
class S2B_NotifyUncompressed:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.NOTIFY]
    """discriminator value"""

    authorization: Optional[str]
    """url: websocket:<nonce>:<ctr>
    
    an empty string is reinterpreted as None for consistency between
    minimal headers mode and expanded headers mode
    """

    identifier: bytes
    """an arbitrary identifier for this notification assigned by the subscriber; max 64 bytes
    """

    compressor_id: Literal[None]
    """discriminator value. We reinterpret a compressor id of 0 to None as we cannot
    type "strictly positive integers" in python for the counterpart to `Literal[0]`
    """

    topic: bytes
    """the topic of the message"""

    verified_uncompressed_sha512: bytes
    """The sha512 hash of the uncompressed message, 64 bytes, verified"""

    uncompressed_message: bytes
    """The message in uncompressed form"""


@fast_dataclass
class S2B_NotifyCompressed:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.NOTIFY]
    """discriminator value"""

    authorization: Optional[str]
    """url: websocket:<nonce>:<ctr>
    
    an empty string is reinterpreted as None for consistency between
    minimal headers mode and expanded headers mode
    """

    identifier: bytes
    """an arbitrary identifier for this notification assigned by the subscriber; max 64 bytes
    """

    compressor_id: int
    """the id of the compressor used to compress the message"""

    topic: bytes
    """the topic of the message"""

    verified_compressed_sha512: bytes
    """The sha512 hash of the compressed message, 64 bytes, verified"""

    compressed_message: bytes
    """The message in compressed form"""

    decompressed_length: int
    """The expected, but unverified, length of the message after decompression"""


S2B_Notify = Union[S2B_NotifyUncompressed, S2B_NotifyCompressed]


_headers: Collection[str] = (
    "authorization",
    "x-identifier",
    "x-topic",
    "x-compressor",
    "x-compressed-length",
    "x-decompressed-length",
    "x-compressed-sha512",
)


class S2B_NotifyParser:
    """Satisfies S2B_MessageParser[S2B_Notify]"""

    @classmethod
    def relevant_types(cls) -> List[SubscriberToBroadcasterStatefulMessageType]:
        return [SubscriberToBroadcasterStatefulMessageType.NOTIFY]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: SubscriberToBroadcasterStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> S2B_Notify:
        assert type == SubscriberToBroadcasterStatefulMessageType.NOTIFY

        headers = parse_simple_headers(flags, payload, _headers)

        authorization_bytes = headers.get("authorization", b"")
        authorization = (
            None if authorization_bytes == b"" else authorization_bytes.decode("utf-8")
        )

        identifier = headers["x-identifier"]
        if len(identifier) > 64:
            raise ValueError("x-identifier must be at most 64 bytes")

        topic = headers["x-topic"]
        compressor_id_bytes = headers["x-compressor"]
        if len(compressor_id_bytes) > 8:
            raise ValueError("x-compressor must be at most 8 bytes")

        compressor_id = int.from_bytes(compressor_id_bytes, "big")

        compressed_length_bytes = headers["x-compressed-length"]
        if len(compressed_length_bytes) > 8:
            raise ValueError("x-compressed-length must be at most 8 bytes")

        compressed_length = int.from_bytes(compressed_length_bytes, "big")

        decompressed_length_bytes = headers["x-decompressed-length"]
        if len(decompressed_length_bytes) > 8:
            raise ValueError("x-decompressed-length must be at most 8 bytes")

        decompressed_length = int.from_bytes(decompressed_length_bytes, "big")

        compressed_sha512 = headers["x-compressed-sha512"]
        if len(compressed_sha512) != 64:
            raise ValueError("x-compressed-sha512 must be 64 bytes")

        message = payload.read(-1)

        if len(message) != compressed_length:
            raise ValueError("x-compressed-length does not match the message length")

        message_digest = hashlib.sha512(message).digest()

        if message_digest != compressed_sha512:
            raise ValueError("x-compressed-sha512 does not match the message")

        if compressor_id == 0:
            if decompressed_length != compressed_length:
                raise ValueError(
                    "x-decompressed-length must equal x-compressed-length if x-compressor is 0"
                )

            return S2B_NotifyUncompressed(
                type=type,
                authorization=authorization,
                identifier=identifier,
                compressor_id=None,
                topic=topic,
                verified_uncompressed_sha512=compressed_sha512,
                uncompressed_message=message,
            )

        return S2B_NotifyCompressed(
            type=type,
            authorization=authorization,
            identifier=identifier,
            compressor_id=compressor_id,
            topic=topic,
            verified_compressed_sha512=compressed_sha512,
            compressed_message=message,
            decompressed_length=decompressed_length,
        )


if TYPE_CHECKING:
    _: Type[S2B_MessageParser[S2B_Notify]] = S2B_NotifyParser


def serialize_s2b_notify(
    msg: S2B_Notify, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[S2B_Notify]"""
    authorization_bytes = (
        b"" if msg.authorization is None else msg.authorization.encode("utf-8")
    )

    if msg.compressor_id is None:
        return serialize_simple_message(
            type=msg.type,
            header_names=_headers,
            header_values=(
                authorization_bytes,
                msg.identifier,
                msg.topic,
                b"\x00",
                int_to_minimal_unsigned(len(msg.uncompressed_message)),
                int_to_minimal_unsigned(len(msg.uncompressed_message)),
                msg.verified_uncompressed_sha512,
            ),
            payload=msg.uncompressed_message,
            minimal_headers=minimal_headers,
        )

    return serialize_simple_message(
        type=msg.type,
        header_names=_headers,
        header_values=(
            authorization_bytes,
            msg.identifier,
            msg.topic,
            int_to_minimal_unsigned(msg.compressor_id),
            int_to_minimal_unsigned(len(msg.compressed_message)),
            int_to_minimal_unsigned(msg.decompressed_length),
            msg.verified_compressed_sha512,
        ),
        payload=msg.compressed_message,
        minimal_headers=minimal_headers,
    )


if TYPE_CHECKING:
    __: MessageSerializer[S2B_Notify] = serialize_s2b_notify
