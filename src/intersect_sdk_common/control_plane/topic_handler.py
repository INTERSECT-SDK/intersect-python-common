"""Attributes associated with a specific pub/sub topic."""

import re

from .definitions import MessageCallback


class TopicHandler:
    """ControlPlaneManager information about a topic, avoids protocol specific information."""

    callbacks: set[MessageCallback]
    """Set of functions to call when consuming a message.

    (In practice there will only be one callback, but it could be helpful to add a debugging function callback in for development.)
    """
    topic_persist: bool
    """Whether or not a topic queue is expected to persist on the message broker."""

    queue_name: str
    """The name of the queue to subscribe to for this topic."""

    _regex_pattern: re.Pattern[str] | None = None
    """If this is a wildcard topic, the regex pattern to match incoming topics against (if no wildcards, this will be None)."""

    def __init__(
        self, topic_persist: bool, queue_name: str, regex_pattern: str | None = None
    ) -> None:
        """Initialize a TopicHandler instance.

        Args:
            topic_persist: Whether the topic queue is expected to persist on the message broker.
            queue_name: The name of the queue to subscribe to for this topic.
            regex_pattern: If this is a wildcard topic, the regex pattern to match incoming topics against (if no wildcards, leave as None).
        """
        self.callbacks = set()
        self.topic_persist = topic_persist
        self.queue_name = queue_name

        if regex_pattern:
            regex_builder = ['^']
            for char in regex_pattern:
                if char == '*':
                    # match a single word (do not include the separator)
                    regex_builder.append('[a-zA-Z0-9-]+')
                elif char == '#':
                    # match any sequence of 0 or more words (make sure to allow for the separator)
                    regex_builder.append('[a-zA-Z0-9/-]*')
                elif char == '/':
                    # in-memory topics use '/' as the separator, it is the protocol handler's responsibility to convert topics to use '/' as the separator
                    regex_builder.append('/')
                else:
                    # ordinary character
                    regex_builder.append(char)
            regex_builder.append('$')
            self._regex_pattern = re.compile(''.join(regex_builder))
        else:
            self._regex_pattern = None

    def does_topic_match(self, topic: str) -> bool:
        """Check if a given topic could be caught by the TopicHandler's topic regex. Only used for wildcard topics."""
        if self._regex_pattern:
            return bool(self._regex_pattern.match(topic))
        return False
