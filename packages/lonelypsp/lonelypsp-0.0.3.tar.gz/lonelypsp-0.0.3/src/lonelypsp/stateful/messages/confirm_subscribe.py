from typing import TYPE_CHECKING, Collection, List, Literal, Type, Union

from lonelypsp.sync_io import SyncReadableBytesIO
from lonelypsp.stateful.constants import (
    BroadcasterToSubscriberStatefulMessageType,
    PubSubStatefulMessageFlags,
)
from lonelypsp.compat import fast_dataclass
from lonelypsp.stateful.generic_parser import B2S_MessageParser
from lonelypsp.stateful.parser_helpers import parse_simple_headers
from lonelypsp.stateful.serializer_helpers import (
    MessageSerializer,
    serialize_simple_message,
)


@fast_dataclass
class B2S_ConfirmSubscribeExact:
    """
    B2S = Broadcaster to Subscriber
    See the type enum documentation for more information on the fields
    """

    type: Literal[BroadcasterToSubscriberStatefulMessageType.CONFIRM_SUBSCRIBE_EXACT]
    """discriminator value"""

    topic: bytes
    """the topic the subscriber is now subscribed to"""


@fast_dataclass
class B2S_ConfirmSubscribeGlob:
    """
    B2S = Broadcaster to Subscriber
    See the type enum documentation for more information on the fields
    """

    type: Literal[BroadcasterToSubscriberStatefulMessageType.CONFIRM_SUBSCRIBE_GLOB]
    """discriminator value"""

    glob: str
    """the glob pattern whose matching topics the subscriber is now subscribed to"""


B2S_ConfirmSubscribe = Union[B2S_ConfirmSubscribeExact, B2S_ConfirmSubscribeGlob]


_exact_headers: Collection[str] = ("x-topic",)


class B2S_ConfirmSubscribeExactParser:
    """Satisfies B2S_MessageParser[B2S_ConfirmSubscribeExact]"""

    @classmethod
    def relevant_types(cls) -> List[BroadcasterToSubscriberStatefulMessageType]:
        return [BroadcasterToSubscriberStatefulMessageType.CONFIRM_SUBSCRIBE_EXACT]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: BroadcasterToSubscriberStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> B2S_ConfirmSubscribeExact:
        assert (
            type == BroadcasterToSubscriberStatefulMessageType.CONFIRM_SUBSCRIBE_EXACT
        )

        headers = parse_simple_headers(flags, payload, _exact_headers)
        topic = headers["x-topic"]
        return B2S_ConfirmSubscribeExact(
            type=type,
            topic=topic,
        )


if TYPE_CHECKING:
    _: Type[B2S_MessageParser[B2S_ConfirmSubscribeExact]] = (
        B2S_ConfirmSubscribeExactParser
    )


def serialize_b2s_confirm_subscribe_exact(
    msg: B2S_ConfirmSubscribeExact, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[B2S_ConfirmSubscribeExact]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_exact_headers,
        header_values=(msg.topic,),
        minimal_headers=minimal_headers,
        payload=b"",
    )


if TYPE_CHECKING:
    __: MessageSerializer[B2S_ConfirmSubscribeExact] = (
        serialize_b2s_confirm_subscribe_exact
    )


_glob_headers: Collection[str] = ("x-glob",)


class B2S_ConfirmSubscribeGlobParser:
    """Satisfies B2S_MessageParser[B2S_ConfirmSubscribeGlob]"""

    @classmethod
    def relevant_types(cls) -> List[BroadcasterToSubscriberStatefulMessageType]:
        return [BroadcasterToSubscriberStatefulMessageType.CONFIRM_SUBSCRIBE_GLOB]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: BroadcasterToSubscriberStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> B2S_ConfirmSubscribeGlob:
        assert type == BroadcasterToSubscriberStatefulMessageType.CONFIRM_SUBSCRIBE_GLOB

        headers = parse_simple_headers(flags, payload, _glob_headers)
        glob = headers["x-glob"].decode("utf-8")
        return B2S_ConfirmSubscribeGlob(
            type=type,
            glob=glob,
        )


if TYPE_CHECKING:
    ___: Type[B2S_MessageParser[B2S_ConfirmSubscribeGlob]] = (
        B2S_ConfirmSubscribeGlobParser
    )


def serialize_b2s_confirm_subscribe_glob(
    msg: B2S_ConfirmSubscribeGlob, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[B2S_ConfirmSubscribeGlob]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_glob_headers,
        header_values=(msg.glob.encode("utf-8"),),
        minimal_headers=minimal_headers,
        payload=b"",
    )


if TYPE_CHECKING:
    ____: MessageSerializer[B2S_ConfirmSubscribeGlob] = (
        serialize_b2s_confirm_subscribe_glob
    )
