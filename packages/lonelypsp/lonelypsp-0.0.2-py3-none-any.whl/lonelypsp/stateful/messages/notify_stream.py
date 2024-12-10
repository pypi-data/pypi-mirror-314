from typing import (
    TYPE_CHECKING,
    Collection,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    Union,
    cast,
)

from lonelypsp.sync_io import SyncReadableBytesIO
from lonelypsp.stateful.constants import (
    PubSubStatefulMessageFlags,
    SubscriberToBroadcasterStatefulMessageType,
)
from lonelypsp.compat import fast_dataclass
from lonelypsp.stateful.generic_parser import S2B_MessageParser
from lonelypsp.stateful.parser_helpers import (
    GeneratorContextManager,
    parse_expanded_headers,
    parse_minimal_message_headers,
)
from lonelypsp.stateful.serializer_helpers import (
    MessageSerializer,
    int_to_minimal_unsigned,
    serialize_simple_message,
)


@fast_dataclass
class S2B_NotifyStreamStartUncompressed:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields

    This type is for when x-part-id is 0 and x-compressor is 0
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.NOTIFY_STREAM]
    """discriminator value"""

    authorization: Optional[str]
    """url: websocket:<nonce>:<ctr>
    
    an empty string is reinterpreted as None for consistency between
    minimal headers mode and expanded headers mode
    """

    identifier: bytes
    """an arbitrary identifier for this notification assigned by the subscriber; max 64 bytes
    """

    part_id: Literal[None]
    """discriminator value. We reinterpret a part id of 0 to None as we cannot
    type "strictly positive integers" in python for the counterpart to `Literal[0]`
    """

    topic: bytes
    """the topic the notification is for"""

    compressor_id: Literal[None]
    """discriminator value. We reinterpret a compressor id of 0 to None as we cannot
    type "strictly positive integers" in python for the counterpart to `Literal[0]`
    """

    uncompressed_length: int
    """the number of bytes that comprise the notification body"""

    unverified_uncompressed_sha512: bytes
    """The unverified sha512 hash of the entire uncompressed notification body, 64 bytes"""

    payload: bytes
    """The first part of the notification in uncompressed form"""


@fast_dataclass
class S2B_NotifyStreamStartCompressed:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields

    This type is for when x-part-id is 0 and x-compressor is not 0
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.NOTIFY_STREAM]
    """discriminator value"""

    authorization: Optional[str]
    """url: websocket:<nonce>:<ctr>
    
    an empty string is reinterpreted as None for consistency between
    minimal headers mode and expanded headers mode
    """

    identifier: bytes
    """an arbitrary identifier for this notification assigned by the subscriber; max 64 bytes
    """

    part_id: Literal[None]
    """discriminator value. We reinterpret a part id of 0 to None as we cannot
    type "strictly positive integers" in python for the counterpart to `Literal[0]`
    """

    topic: bytes
    """the topic the notification is for"""

    compressor_id: int
    """a positive value indicating which compressor was used to compress the message"""

    compressed_length: int
    """the number of bytes that comprise the compressed notification body"""

    decompressed_length: int
    """when decompressing the compressed data, the number of bytes that should be produced"""

    unverified_compressed_sha512: bytes
    """the unverified sha512 hash of the entire compressed notification body, 64 bytes"""

    payload: bytes
    """the first part of the notification in compressed form; the compression is over the
    entire notification body, so this is probably not decompressible by itself
    """


@fast_dataclass
class S2B_NotifyStreamContinuation:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields

    This type is for when x-part-id is not 0
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.NOTIFY_STREAM]
    """discriminator value"""

    authorization: Optional[str]
    """url: websocket:<nonce>:<ctr>
    
    an empty string is reinterpreted as None for consistency between
    minimal headers mode and expanded headers mode
    """

    identifier: bytes
    """an arbitrary identifier for this notification assigned by the subscriber; max 64 bytes
    """

    part_id: int
    """a positive value indicating the part number of the message. never sent out of order"""

    payload: bytes
    """the additional payload data for the notification"""


S2B_NotifyStream = Union[
    S2B_NotifyStreamStartUncompressed,
    S2B_NotifyStreamStartCompressed,
    S2B_NotifyStreamContinuation,
]

_basic_headers: Collection[str] = (
    "authorization",
    "x-identifier",
    "x-part-id",
)

_start_headers: Collection[str] = (
    "x-topic",
    "x-compressor",
    "x-compressed-length",
    "x-decompressed-length",
    "x-compressed-sha512",
)

_total_start_headers: Collection[str] = cast(List[str], _basic_headers) + cast(
    List[str], _start_headers
)


class S2B_NotifyStreamParser:
    """Satisfies S2B_MessageParser[S2B_NotifyStream]"""

    @classmethod
    def relevant_types(cls) -> List[SubscriberToBroadcasterStatefulMessageType]:
        return [SubscriberToBroadcasterStatefulMessageType.NOTIFY_STREAM]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: SubscriberToBroadcasterStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> S2B_NotifyStream:
        assert type == SubscriberToBroadcasterStatefulMessageType.NOTIFY_STREAM
        headers: Dict[str, bytes] = dict()

        if (flags & PubSubStatefulMessageFlags.MINIMAL_HEADERS) != 0:
            with GeneratorContextManager(
                parse_minimal_message_headers(payload)
            ) as parser:
                headers["authorization"] = next(parser)
                headers["x-identifier"] = next(parser)

                part_id_bytes = next(parser)
                if len(part_id_bytes) > 8:
                    raise ValueError("x-part-id must be at most 8 bytes")

                headers["x-part-id"] = part_id_bytes

                part_id = int.from_bytes(part_id_bytes, "big")

                if part_id == 0:
                    for header_name in _start_headers:
                        headers[header_name] = next(parser)
        else:
            headers = parse_expanded_headers(payload)

        authorization_bytes = headers.get("authorization", b"")
        authorization = (
            None if authorization_bytes == b"" else authorization_bytes.decode("utf-8")
        )

        identifier = headers["x-identifier"]
        if len(identifier) > 64:
            raise ValueError("x-identifier must be at most 64 bytes")

        part_id_bytes = headers["x-part-id"]
        if len(part_id_bytes) > 8:
            raise ValueError("x-part-id must be at most 8 bytes")

        part_id = int.from_bytes(part_id_bytes, "big")

        if part_id > 0:
            return S2B_NotifyStreamContinuation(
                type=type,
                authorization=authorization,
                identifier=identifier,
                part_id=part_id,
                payload=payload.read(-1),
            )

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

        if compressor_id == 0:
            if compressed_length != decompressed_length:
                raise ValueError(
                    "decompressed length must equal compressed length when x-compressor is 0"
                )

            return S2B_NotifyStreamStartUncompressed(
                type=type,
                authorization=authorization,
                identifier=identifier,
                part_id=None,
                topic=topic,
                compressor_id=None,
                uncompressed_length=compressed_length,
                unverified_uncompressed_sha512=compressed_sha512,
                payload=payload.read(-1),
            )

        return S2B_NotifyStreamStartCompressed(
            type=type,
            authorization=authorization,
            identifier=identifier,
            part_id=None,
            topic=topic,
            compressor_id=compressor_id,
            compressed_length=compressed_length,
            decompressed_length=decompressed_length,
            unverified_compressed_sha512=compressed_sha512,
            payload=payload.read(-1),
        )


if TYPE_CHECKING:
    _: Type[S2B_MessageParser[S2B_NotifyStream]] = S2B_NotifyStreamParser


def serialize_s2b_notify_stream(
    msg: S2B_NotifyStream, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[S2B_NotifyStream]"""
    authorization_bytes = (
        msg.authorization.encode("utf-8") if msg.authorization is not None else b""
    )

    if msg.part_id is not None:
        return serialize_simple_message(
            type=msg.type,
            header_names=_basic_headers,
            header_values=(
                authorization_bytes,
                msg.identifier,
                int_to_minimal_unsigned(msg.part_id),
            ),
            payload=msg.payload,
            minimal_headers=minimal_headers,
        )

    if msg.compressor_id is None:
        return serialize_simple_message(
            type=msg.type,
            header_names=_total_start_headers,
            header_values=(
                authorization_bytes,
                msg.identifier,
                b"\x00",
                msg.topic,
                b"\x00",
                int_to_minimal_unsigned(msg.uncompressed_length),
                msg.unverified_uncompressed_sha512,
            ),
            payload=msg.payload,
            minimal_headers=minimal_headers,
        )

    return serialize_simple_message(
        type=msg.type,
        header_names=_total_start_headers,
        header_values=(
            authorization_bytes,
            msg.identifier,
            b"\x00",
            msg.topic,
            int_to_minimal_unsigned(msg.compressor_id),
            int_to_minimal_unsigned(msg.compressed_length),
            int_to_minimal_unsigned(msg.decompressed_length),
            msg.unverified_compressed_sha512,
        ),
        payload=msg.payload,
        minimal_headers=minimal_headers,
    )


if TYPE_CHECKING:
    __: MessageSerializer[S2B_NotifyStream] = serialize_s2b_notify_stream
