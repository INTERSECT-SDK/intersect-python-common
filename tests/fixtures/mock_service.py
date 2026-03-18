"""This is a dedicated mock service for testing common modules. It should NOT be seen as representative of how services should be implemented, and is only intended to be used for testing purposes."""

import uuid

from intersect_sdk_common import ControlPlaneConfig, ControlPlaneManager, IntersectDataHandler
from intersect_sdk_common.control_plane.messages.userspace import create_userspace_message_headers


class MockService:
    """A mock service for testing purposes."""

    def __init__(self, config: ControlPlaneConfig, channels: list[str]) -> None:
        self.control_plane_manager = ControlPlaneManager(control_configs=[config])
        queue_name = str(uuid.uuid4())
        # make multiple queues to ensure we make sure messages are directed to the appropriate queues
        for channel in channels:
            self.control_plane_manager.add_subscription_channel(
                channel, {self.on_message}, True, queue_name
            )

    def on_message(self, message: bytes, content_type: str, headers: dict[str, str]) -> None:
        # this mock service will do nothing but reverse the message and send it back
        reply_message = message[::-1]
        reply_headers = create_userspace_message_headers(
            headers['destination'],
            headers['source'],
            headers['operation_id'],
            IntersectDataHandler.MESSAGE,
            uuid.UUID(headers['campaign_id']),
            uuid.UUID(headers['request_id']),
        )
        content_type = 'text/plain'
        self.control_plane_manager.publish_message(
            headers['source'], reply_message, content_type, reply_headers, True
        )

    def connect(self) -> None:
        self.control_plane_manager.connect()

    def disconnect(self) -> None:
        self.control_plane_manager.disconnect()
