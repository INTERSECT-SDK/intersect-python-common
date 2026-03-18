"""This is a dedicated mock service for testing common modules. It should NOT be seen as representative of how services should be implemented, and is only intended to be used for testing purposes."""

import threading
import uuid

from intersect_sdk_common import ControlPlaneConfig, ControlPlaneManager, IntersectDataHandler
from intersect_sdk_common.control_plane.messages.userspace import create_userspace_message_headers


class MockClient:
    """A mock client for testing purposes."""

    def __init__(self, config: ControlPlaneConfig, client_sub_channel: str) -> None:
        self.control_plane_manager = ControlPlaneManager(control_configs=[config])
        self.campaign_id = uuid.uuid4()
        self.event = threading.Event()
        self.received_value = (b'', 'application/octet-stream', {})
        self.client_sub_channel = client_sub_channel

        self.control_plane_manager.add_subscription_channel(
            self.client_sub_channel, {self.on_message}, True, str(uuid.uuid4())
        )

    def publish_message(self, channel: str, message: bytes) -> None:
        """publish a message

        NOTE: only supports raw bytes and always uses 'text/plain' as the content type for simplicity.
        NOTE: can only handle one message at a time in the on_message callback, so make sure to wait until the previous message is received before publishing another one.
        """
        # in case you want to reuse this Client again, reset the event
        self.event.clear()
        headers = create_userspace_message_headers(
            source=self.client_sub_channel.replace('/', '.'),
            destination=channel.replace('/', '.'),
            operation_id='operation_not_used',
            data_handler=IntersectDataHandler.MESSAGE,
            campaign_id=self.campaign_id,
            request_id=uuid.uuid4(),
        )
        self.control_plane_manager.publish_message(channel, message, 'text/plain', headers, True)

    def wait(self, timeout: float) -> None:
        self.event.wait(timeout)
        if not self.event.is_set():
            msg = 'Time limit exceeded'
            raise TimeoutError(msg)

    def on_message(self, message: bytes, content_type: str, headers: dict[str, str]) -> None:
        self.received_value = (message, content_type, headers)
        self.event.set()

    def connect(self) -> None:
        self.control_plane_manager.connect()

    def disconnect(self) -> None:
        self.control_plane_manager.disconnect()

    def get_received_value(self) -> tuple[bytes, str, dict[str, str]]:
        return self.received_value
