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
    serialize_simple_message,
)


@fast_dataclass
class S2B_SubscribeExact:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.SUBSCRIBE_EXACT]
    """discriminator value"""

    authorization: Optional[str]
    """url: websocket:<nonce>:<ctr>
    
    an empty string is reinterpreted as None for consistency between
    minimal headers mode and expanded headers mode
    """

    topic: bytes
    """the topic to subscribe to"""


_exact_headers: Collection[str] = ("authorization", "x-topic")


class S2B_SubscribeExactParser:
    """Satisfies S2B_MessageParser[S2B_SubscribeExact]"""

    @classmethod
    def relevant_types(cls) -> List[SubscriberToBroadcasterStatefulMessageType]:
        return [SubscriberToBroadcasterStatefulMessageType.SUBSCRIBE_EXACT]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: SubscriberToBroadcasterStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> S2B_SubscribeExact:
        assert type == SubscriberToBroadcasterStatefulMessageType.SUBSCRIBE_EXACT

        headers = parse_simple_headers(flags, payload, _exact_headers)
        authorization_bytes = headers.get("authorization", b"")
        authorization = (
            None if not authorization_bytes else authorization_bytes.decode("utf-8")
        )

        topic = headers["x-topic"]
        return S2B_SubscribeExact(
            type=type,
            authorization=authorization,
            topic=topic,
        )


if TYPE_CHECKING:
    _: Type[S2B_MessageParser[S2B_SubscribeExact]] = S2B_SubscribeExactParser


def serialize_s2b_subscribe_exact(
    msg: S2B_SubscribeExact, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[S2B_SubscribeExact]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_exact_headers,
        header_values=(
            b"" if msg.authorization is None else msg.authorization.encode("utf-8"),
            msg.topic,
        ),
        minimal_headers=minimal_headers,
        payload=b"",
    )


if TYPE_CHECKING:
    __: MessageSerializer[S2B_SubscribeExact] = serialize_s2b_subscribe_exact


@fast_dataclass
class S2B_SubscribeGlob:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.SUBSCRIBE_GLOB]
    """discriminator value"""

    authorization: Optional[str]
    """url: websocket:<nonce>:<ctr>
    
    an empty string is reinterpreted as None for consistency between
    minimal headers mode and expanded headers mode
    """

    glob: str
    """the glob pattern to subscribe to"""


_glob_headers: Collection[str] = ("authorization", "x-glob")


class S2B_SubscribeGlobParser:
    """Satisfies S2B_MessageParser[S2B_SubscribeGlob]"""

    @classmethod
    def relevant_types(cls) -> List[SubscriberToBroadcasterStatefulMessageType]:
        return [SubscriberToBroadcasterStatefulMessageType.SUBSCRIBE_GLOB]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: SubscriberToBroadcasterStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> S2B_SubscribeGlob:
        assert type == SubscriberToBroadcasterStatefulMessageType.SUBSCRIBE_GLOB

        headers = parse_simple_headers(flags, payload, _glob_headers)
        authorization_bytes = headers.get("authorization", b"")
        authorization = (
            None if not authorization_bytes else authorization_bytes.decode("utf-8")
        )

        glob = headers["x-glob"].decode("utf-8")
        return S2B_SubscribeGlob(
            type=type,
            authorization=authorization,
            glob=glob,
        )


if TYPE_CHECKING:
    ___: Type[S2B_MessageParser[S2B_SubscribeGlob]] = S2B_SubscribeGlobParser


def serialize_s2b_subscribe_glob(
    msg: S2B_SubscribeGlob, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[S2B_SubscribeGlob]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_glob_headers,
        header_values=(
            b"" if msg.authorization is None else msg.authorization.encode("utf-8"),
            msg.glob.encode("utf-8"),
        ),
        minimal_headers=minimal_headers,
        payload=b"",
    )


if TYPE_CHECKING:
    ____: MessageSerializer[S2B_SubscribeGlob] = serialize_s2b_subscribe_glob

S2B_Subscribe = Union[S2B_SubscribeExact, S2B_SubscribeGlob]
