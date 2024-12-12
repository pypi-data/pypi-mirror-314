from dataclasses import dataclass
from typing import TYPE_CHECKING, Collection, List, Literal, Type, Union

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
class S2B_ConfirmReceive:
    """
    S2B = Subscriber to Broadcaster
    See the type enum documentation for more information on the fields
    """

    type: Literal[SubscriberToBroadcasterStatefulMessageType.CONFIRM_RECEIVE]
    """discriminator value"""

    identifier: bytes
    """an arbitrary identifier for the notification assigned by the broadcaster; max 64 bytes
    """


_headers: Collection[str] = ("x-identifier",)


class S2B_ConfirmRecieveParser:
    """Satisfies S2B_MessageParser[S2B_ConfirmReceive]"""

    @classmethod
    def relevant_types(cls) -> List[SubscriberToBroadcasterStatefulMessageType]:
        return [SubscriberToBroadcasterStatefulMessageType.CONFIRM_RECEIVE]

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: SubscriberToBroadcasterStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> S2B_ConfirmReceive:
        assert type == SubscriberToBroadcasterStatefulMessageType.CONFIRM_RECEIVE

        headers = parse_simple_headers(flags, payload, _headers)
        identifier = headers["x-identifier"]
        if len(identifier) > 64:
            raise ValueError("x-identifier must be at most 64 bytes")

        return S2B_ConfirmReceive(
            type=type,
            identifier=identifier,
        )


if TYPE_CHECKING:
    _: Type[S2B_MessageParser[S2B_ConfirmReceive]] = S2B_ConfirmRecieveParser


def serialize_s2b_confirm_receive(
    msg: S2B_ConfirmReceive, /, *, minimal_headers: bool
) -> Union[bytes, bytearray, memoryview]:
    """Satisfies MessageSerializer[S2B_ConfirmReceive]"""
    return serialize_simple_message(
        type=msg.type,
        header_names=_headers,
        header_values=(msg.identifier,),
        payload=b"",
        minimal_headers=minimal_headers,
    )


if TYPE_CHECKING:
    __: MessageSerializer[S2B_ConfirmReceive] = serialize_s2b_confirm_receive
