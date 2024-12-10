from enum import IntEnum, auto


class SubscriberToBroadcasterStatelessMessageType(IntEnum):
    """Assigns a unique integer to each type of message that a subscriber can
    send to a broadcaster over a stateless connection. The prototypical example
    of a stateless connection would be using a distinct HTTP call for each
    message.

    Because stateless connections generally already have more parsing helpers available,
    we just provide documentation on how the message should be structured, but don't
    actually provide parsers or serializers.
    """

    NOTIFY = auto()
    """The subscriber is posting a message to a specific topic
    
    ### headers
    - authorization: proof the subscriber is authorized to post to the topic

    ### body
    - 2 bytes (N): length of the topic, big-endian, unsigned
    - N bytes: the topic. if utf-8 decodable then we will attempt to match glob
      patterns, otherwise, only goes to exact subscriptions
    - 64 bytes: sha-512 hash of the message, will be rechecked
    - 8 bytes (M): length of the message, big-endian, unsigned
    - M bytes: the message
    """

    SUBSCRIBE_EXACT = auto()
    """The subscriber wants to receive messages posted to a specific topic

    ### headers
    - authorization: proof the subscriber is authorized to subscribe to the topic

    ### body
    - 2 bytes (N): length of the url that the subscriber can be reached at, big-endian, unsigned
    - N bytes: the url that the subscriber can be reached at, utf-8 encoded
    - 2 bytes (M): the length of the topic, big-endian, unsigned
    - M bytes: the topic, utf-8 encoded
    """

    SUBSCRIBE_GLOB = auto()
    """The subscriber wants to receive messages to utf-8 decodable topics which match
    a given glob pattern
    
    ### headers
    - authorization: proof the subscriber is authorized to subscribe to the pattern

    ### body
    - 2 bytes (N): length of the url that the subscriber can be reached at, big-endian, unsigned
    - N bytes: the url that the subscriber can be reached at, utf-8 encoded
    - 2 bytes (M): the length of the glob pattern, big-endian, unsigned
    - M bytes: the glob pattern, utf-8 encoded
    """

    UNSUBSCRIBE_EXACT = auto()
    """The subscriber wants to stop receiving messages posted to a specific topic

    ### headers
    - authorization: proof the subscriber is authorized to unsubscribe from the topic;
      formed exactly like the authorization header in SUBSCRIBE_EXACT
    
    ### body
    - 2 bytes (N): length of the url that the subscriber can be reached at, big-endian, unsigned
    - N bytes: the url that the subscriber can be reached at, utf-8 encoded
    - 2 bytes (M): the length of the topic, big-endian, unsigned
    - M bytes: the topic, utf-8 encoded
    """

    UNSUBSCRIBE_GLOB = auto()
    """The subscriber wants to stop receiving messages to utf-8 decodable topics which match
    a given glob pattern

    ### headers
    - authorization: proof the subscriber is authorized to unsubscribe from the pattern;
      formed exactly like the authorization header in SUBSCRIBE_GLOB

    ### body
    - 2 bytes (N): length of the url that the subscriber can be reached at, big-endian, unsigned
    - N bytes: the url that the subscriber can be reached at, utf-8 encoded
    - 2 bytes (M): the length of the glob pattern, big-endian, unsigned
    - M bytes: the glob pattern, utf-8 encoded
    """


class SubscriberToBroadcasterStatelessResponseType(IntEnum):
    """When the broadcaster reaches out to a subscriber they have the opportunity
    to respond with one of these types of messages, without headers
    """

    UNKNOWN = auto()
    """Used when no specific meaning was understood about the response"""

    UNSUBSCRIBE_IMMEDIATE = auto()
    """When sent in response to a RECEIVE message, removes whatever subscription
    caused the subscriber to receive the message

    The body is a json object with at least the following keys:
    - `unsubscribe`: the value `true`

    All other values are ignored, however, a common one worth mentioning is:
    - `reason`: a human-readable string indicating if the subscriber didn't
      like the format of the message vs just wasn't expecting a message on that
      topic vs was expecting the message but no longer wants more
    """


class BroadcasterToSubscriberStatelessMessageType(IntEnum):
    """Assigns a unique integer to each type of message that a broadcaster can
    send to a subscriber over a stateless connection. The prototypical example
    of a stateless connection would be using a distinct HTTP call for each
    message.
    """

    RECEIVE = auto()
    """The broadcaster is notifying the subscriber of a message posted to a topic
    
    ### headers
    - authorization: proof the broadcaster can notify the subscriber
    - repr-digest: contains <digest-algorithm>=<digest>[,<digest-algorithm>=<digest>...]
      where at least one of the digest algorithms is `sha512` and the digest is the
      the base64 encoded sha-512 hash of the message
    - x-topic: the topic the message was posted to

    ### body
    the message that was posted to the topic
    """
