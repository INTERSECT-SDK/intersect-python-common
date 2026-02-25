"""Attributes associated with a specific pub/sub topic."""

from collections.abc import Callable

from .definitions import MessageCallback


class TopicHandler:
    """ControlPlaneManager information about a topic, avoids protocol specific information."""

    callbacks: set[MessageCallback]
    """Set of functions to call when consuming a message.

    (In practice there will only be one callback, but it could be helpful to add a debugging function callback in for development.)
    """
    topic_persist: bool
    """Whether or not a topic queue is expected to persist on the message broker."""

    queue_name_generator: Callable[[str], str]
    """A pointer to the function which generates the queue name.."""

    def __init__(self, topic_persist: bool, queue_name_generator: Callable[[str], str]) -> None:
        """Initialize a TopicHandler instance.

        Args:
            topic_persist: Whether the topic queue is expected to persist on the message broker.
            queue_name_generator: A pointer to the function which generates the queue name.
        """
        self.callbacks = set()
        self.topic_persist = topic_persist
        self.queue_name_generator = queue_name_generator
