from unittest.mock import MagicMock

import pika.exceptions
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.reasoncodes import ReasonCode

from intersect_sdk_common.config import ControlPlaneConfig
from intersect_sdk_common.control_plane.control_plane_manager import ControlPlaneManager


def _config(protocol: str, password: str) -> ControlPlaneConfig:
    return ControlPlaneConfig(
        protocol=protocol,  # type: ignore[arg-type]
        system_name='system',
        username='user',
        password=password,
    )


def test_amqp_refreshes_credentials_on_auth_error():
    refresher = MagicMock(return_value=_config('amqp0.9.1', 'new'))
    manager = ControlPlaneManager([_config('amqp0.9.1', 'old')], refresher)
    client = manager._control_providers[0]

    client._on_connection_open_error(MagicMock(), pika.exceptions.ProbableAuthenticationError())
    assert client.credentials_invalid()
    assert manager.credentials_invalid()
    refresher.assert_called_once_with('system')
    assert client._connection_params.credentials.password == 'new'  # noqa: S105

    refresher.reset_mock()
    client._on_connection_open_error(MagicMock(), pika.exceptions.AMQPConnectionError())
    assert not client.credentials_invalid()
    refresher.assert_not_called()


def test_mqtt_refreshes_credentials_on_auth_error():
    refresher = MagicMock(return_value=_config('mqtt5.0', 'new'))
    manager = ControlPlaneManager([_config('mqtt5.0', 'old')], refresher)
    client = manager._control_providers[0]

    client._handle_connect(
        client._connection, None, {}, ReasonCode(PacketTypes.CONNACK, identifier=134), None
    )
    assert client.credentials_invalid()
    refresher.assert_called_once_with('system')
    assert client._connection._password == b'new'


def test_refresher_exception_keeps_old_config():
    manager = ControlPlaneManager(
        [_config('amqp0.9.1', 'old')], MagicMock(side_effect=RuntimeError('registry down'))
    )
    client = manager._control_providers[0]
    client._on_connection_open_error(MagicMock(), pika.exceptions.ProbableAuthenticationError())
    assert client.credentials_invalid()
    assert client._connection_params.credentials.password == 'old'  # noqa: S105
