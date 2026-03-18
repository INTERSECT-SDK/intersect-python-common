import time

import pytest

from intersect_sdk_common import ControlPlaneConfig, ControlProvider

from ..fixtures.mock_client import MockClient
from ..fixtures.mock_service import MockService


def get_config(protocol: ControlProvider, port: int) -> ControlPlaneConfig:
    return ControlPlaneConfig(
        protocol=protocol,
        username='intersect_username',
        password='intersect_password',
        host='127.0.0.1',
        port=port,
    )


# IMPORTANT: make sure that at least one channel topic is unique between test cases per client and service, otherwise messages may not be handled properly on the brokers
@pytest.mark.parametrize(
    ('protocol', 'port', 'client_pub_channel', 'svc_sub_channel', 'client_sub_channel'),
    [
        # no wildcards (this should be used in 99.99% of use cases across the INTERSECT ecosystem)
        (
            'amqp0.9.1',
            5672,
            'org/fac/sys/sub/svc/test-subscription-strings-svc-1',
            'org/fac/sys/sub/svc/test-subscription-strings-svc-1',
            'org/fac/sys/sub/svc/test-subscription-strings-client-1',
        ),
        (
            'mqtt5.0',
            1883,
            'org/fac/sys/sub/svc/test-subscription-strings-svc-2',
            'org/fac/sys/sub/svc/test-subscription-strings-svc-2',
            'org/fac/sys/sub/svc/test-subscription-strings-client-2',
        ),
        # single-level wildcards, needed for iHub
        (
            'amqp0.9.1',
            5672,
            'org/fac/sys/sub/svc/test-subscription-strings-svc-3',
            '*/*/*/*/*/test-subscription-strings-svc-3',
            'tmp/tmp/tmp/tmp/tmp/test-subscription-strings-client-3',
        ),
        (
            'mqtt5.0',
            1883,
            'org/fac/sys/sub/svc/test-subscription-strings-svc-4',
            '*/*/*/*/*/test-subscription-strings-svc-4',
            'tmp/tmp/tmp/tmp/tmp/test-subscription-strings-client-4',
        ),
        (
            'amqp0.9.1',
            5672,
            'org/fac/test-subscription-strings-svc-5/sys/sub/svc',
            '*/*/test-subscription-strings-svc-5/*/*/*',
            'tmp/tmp/tmp/tmp/tmp/test-subscription-strings-client-5',
        ),
        (
            'mqtt5.0',
            1883,
            'org/fac/test-subscription-strings-svc-6/sys/sub/svc',
            '*/*/test-subscription-strings-svc-6/*/*/*',
            'tmp/tmp/tmp/tmp/tmp/test-subscription-strings-client-6',
        ),
        # multi-level wildcards, not needed in ecosystem for the moment (NOTE: multi-level wildcards can only be used at the end of the topic string according to MQTT spec, so we put it at the end here to ensure that the test is valid for both AMQP and MQTT)
        (
            'amqp0.9.1',
            5672,
            'test-subscription-strings-svc-7/whatever/required/hierarchy/path',
            'test-subscription-strings-svc-7/*/required/#',
            'tmp/tmp/tmp/tmp/tmp/test-subscription-strings-client-7',
        ),
        (
            'mqtt5.0',
            1883,
            'test-subscription-strings-svc-8/whatever/required/hierarchy/path',
            'test-subscription-strings-svc-8/*/required/#',
            'tmp/tmp/tmp/tmp/tmp/test-subscription-strings-client-8',
        ),
    ],
)
def test_subscription_strings(
    protocol: ControlProvider,
    port: int,
    client_pub_channel: str,
    svc_sub_channel: str,
    client_sub_channel: str,
) -> None:
    """Test that wildcard subscriptions are properly matched and receive messages."""
    service_config = get_config(protocol, port)
    client_config = get_config(protocol, port)

    mock_service = MockService(service_config, [svc_sub_channel])
    mock_client = MockClient(client_config, client_sub_channel)
    try:
        mock_service.connect()
        mock_client.connect()

        if protocol == 'amqp0.9.1':
            # NOTE: for AMQP, we need to wait a bit to ensure that basic_consume has been established with the broker through ControlPlaneManager before we publish the message
            time.sleep(1.0)

        # begin request/reply pattern and wait until we get it back
        mock_client.publish_message(
            client_pub_channel, b'the quick brown fox jumps over the lazy dog'
        )
        mock_client.wait(10.0)

        received_message, content_type, headers = mock_client.get_received_value()
        assert received_message == b'god yzal eht revo spmuj xof nworb kciuq eht'
        assert content_type == 'text/plain'
        assert headers['source'] == client_pub_channel.replace('/', '.')
    finally:
        mock_service.disconnect()
        mock_client.disconnect()
