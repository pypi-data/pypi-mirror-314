from typing import Generic, List, Protocol, TypeVar

from lonelypsp.stateful.constants import (
    BroadcasterToSubscriberStatefulMessageType,
    PubSubStatefulMessageFlags,
    SubscriberToBroadcasterStatefulMessageType,
)

from lonelypsp.sync_io import SyncReadableBytesIO


T_co = TypeVar("T_co", covariant=True)


class S2B_MessageParser(Generic[T_co], Protocol):
    """Describes something that can parse a message from a subscriber to a broadcaster"""

    @classmethod
    def relevant_types(cls) -> List[SubscriberToBroadcasterStatefulMessageType]:
        """Returns the list of messages that this parser can parse"""
        ...

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: SubscriberToBroadcasterStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> T_co:
        """Parses a message from a subscriber to a broadcaster

        Args:
            flags (PubSubStatefulMessageFlags): the flags for the message
            type (SubscriberToBroadcasterStatefulMessageType): the type of the message
            payload (IO[bytes]): the payload of the message, seeked to after the
                type (i.e,. at the start of the payload)

        Returns:
            T: the parsed message

        Raises:
            AssertionError: if type is not in relevant_types
            ValueError: if the message is malformed
        """
        ...


class B2S_MessageParser(Generic[T_co], Protocol):
    """Describes something that can parse a message from a broadcaster to a subscriber"""

    @classmethod
    def relevant_types(cls) -> List[BroadcasterToSubscriberStatefulMessageType]:
        """Returns the list of messages that this parser can parse"""
        ...

    @classmethod
    def parse(
        cls,
        flags: PubSubStatefulMessageFlags,
        type: BroadcasterToSubscriberStatefulMessageType,
        payload: SyncReadableBytesIO,
    ) -> T_co:
        """Parses a message from a broadcaster to a subscriber

        Args:
            flags (PubSubStatefulMessageFlags): the flags for the message
            type (BroadcasterToSubscriberStatefulMessageType): the type of the message
            payload (readable file-like): the payload of the message, seeked to after the
                type (i.e,. at the start of the payload)

        Returns:
            T: the parsed message

        Raises:
            AssertionError: if type is not in relevant_types
            ValueError: if the message is malformed
        """
        ...
