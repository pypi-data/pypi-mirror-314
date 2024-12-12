from typing import Union

from lonelypsp.stateful.messages.configure import S2B_Configure
from lonelypsp.stateful.messages.confirm_configure import B2S_ConfirmConfigure
from lonelypsp.stateful.messages.confirm_notify import B2S_ConfirmNotify
from lonelypsp.stateful.messages.confirm_receive import S2B_ConfirmReceive
from lonelypsp.stateful.messages.confirm_subscribe import (
    B2S_ConfirmSubscribeExact,
    B2S_ConfirmSubscribeGlob,
)
from lonelypsp.stateful.messages.confirm_unsubscribe import (
    B2S_ConfirmUnsubscribeExact,
    B2S_ConfirmUnsubscribeGlob,
)
from lonelypsp.stateful.messages.continue_notify import B2S_ContinueNotify
from lonelypsp.stateful.messages.continue_receive import S2B_ContinueReceive
from lonelypsp.stateful.messages.enable_zstd_custom import B2S_EnableZstdCustom
from lonelypsp.stateful.messages.enable_zstd_preset import B2S_EnableZstdPreset
from lonelypsp.stateful.messages.notify_stream import S2B_NotifyStream
from lonelypsp.stateful.messages.notify import S2B_Notify
from lonelypsp.stateful.messages.receive_stream import B2S_ReceiveStream
from lonelypsp.stateful.messages.subscribe import (
    S2B_SubscribeExact,
    S2B_SubscribeGlob,
)
from lonelypsp.stateful.messages.unsubscribe import (
    S2B_UnsubscribeExact,
    S2B_UnsubscribeGlob,
)


S2B_Message = Union[
    S2B_Configure,
    S2B_ConfirmReceive,
    S2B_ContinueReceive,
    S2B_NotifyStream,
    S2B_Notify,
    S2B_SubscribeExact,
    S2B_SubscribeGlob,
    S2B_UnsubscribeExact,
    S2B_UnsubscribeGlob,
]
"""Type alias for any message from a subscriber to a broadcaster"""

B2S_Message = Union[
    B2S_ConfirmConfigure,
    B2S_ConfirmNotify,
    B2S_ConfirmSubscribeExact,
    B2S_ConfirmSubscribeGlob,
    B2S_ConfirmUnsubscribeExact,
    B2S_ConfirmUnsubscribeGlob,
    B2S_ContinueNotify,
    B2S_EnableZstdCustom,
    B2S_EnableZstdPreset,
    B2S_ReceiveStream,
]
"""Type alias for any message from a broadcaster to a subscriber"""
