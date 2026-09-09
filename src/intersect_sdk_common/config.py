"""Configuration types shared across both Clients and Services."""

from dataclasses import dataclass, field
from typing import Annotated, Literal

from pydantic import BaseModel, Field, PositiveInt

from .core_definitions import IntersectDataHandler

HIERARCHY_REGEX = r'[a-z0-9][-a-z0-9]{2,62}'
"""
The hierarchy regex should accomplish the following:

- Only allow unreserved characters (alphanumeric and .-~_): https://datatracker.ietf.org/doc/html/rfc3986#section-2.3
- Require lowercase letters to avoid incompatibilities with case-insensitive systems.
- Range should be from 3-63 characters
- Be CLI friendly (don't start with hyphen) and URI friendly (don't use underscores)

This enables maximum integration with other systems (i.e. MINIO) without having to transform the hierarchy.
"""
# HIERARCHY_REGEX = r'^[a-z0-9]((?!--)[a-z0-9-]){2,62}$'
# If using this regex, you must configure the Pydantic ConfigDict regex_engine to be 'python-re' to support lookaheads
# Used to disallow multiple hyphens
# should work in HTML5 forms out of the gate

ControlProvider = Literal['mqtt5.0', 'amqp0.9.1']
"""The type of broker we connect to."""


@dataclass
class ControlPlaneConfig:
    """Configuration for interacting with a broker."""

    protocol: ControlProvider
    """
    The protocol of the broker you'd like to use (i.e. AMQP, MQTT...)
    """
    # TODO - support more protocols and protocol versions as needed - see https://www.asyncapi.com/docs/reference/specification/v2.6.0#serverObject

    username: Annotated[str, Field(min_length=1)]
    """
    Username credentials for broker connection.
    """

    password: Annotated[str, Field(min_length=1)]
    """
    Password credentials for broker connection.
    """

    host: Annotated[str, Field(min_length=1)] = '127.0.0.1'
    """
    Broker hostname (default: 127.0.0.1)
    """

    port: PositiveInt | None = None
    """
    Broker port. List of common ports:

    - 1883 (MQTT)
    - 4222 (NATS default port)
    - 5222 (XMPP)
    - 5223 (XMPP over TLS)
    - 5671 (AMQP over TLS)
    - 5672 (AMQP)
    - 7400 (DDS Discovery)
    - 7401 (DDS User traffic)
    - 8883 (MQTT over TLS)
    - 61613 (RabbitMQ STOMP - WARNING: ephemeral port)

    NOTE: INTERSECT currently only supports AMQP and MQTT.
    """

    # TODO default this to False once the registry service is in place
    is_root: bool = True
    """
    Whether or not the broker credentials are for connecting as a root user.

    This should be True IF:
      - You are a Core Service
      - You are an SDK Client or Service, but your message broker is hosted locally.

      This should be False IF:
        - You are an SDK Client or Service, and the broker you're connected to is remote.

    This is important for specific implementations; the Registry Service configures queues for microservices, but Core Services configure their own queues themselves.
    """


@dataclass
class DataStoreConfig:
    """Configuration for interacting with a data store."""

    username: Annotated[str, Field(min_length=1)]
    """
    Username credentials for data store connection.
    """

    password: Annotated[str, Field(min_length=1)]
    """
    Password credentials for data store connection.
    """

    host: Annotated[str, Field(min_length=1)] = '127.0.0.1'
    """
    Data store hostname (default: 127.0.0.1)
    """

    port: PositiveInt | None = None
    """
    Data store port
    """


@dataclass
class DataStoreConfigMap:
    """Configurations for any data stores the application should talk to."""

    minio: list[DataStoreConfig] = field(default_factory=list)
    """
    minio configurations
    """

    def get_missing_data_store_types(self) -> set[IntersectDataHandler]:
        """Return a set of IntersectDataHandlers which will not be permitted, due to a configuration type missing.

        If all data configurations exist, returns an empty set
        """
        missing = set()
        if not self.minio:
            missing.add(IntersectDataHandler.MINIO)
        return missing


class IntersectConfig(BaseModel):
    """The response type used by INTERSECT-SDK Services and Clients to understand how to connect to the INTERSECT ecosystem.

    This object should only be used by the SDK, and not users directly.
    """

    system_name: Annotated[str, Field(pattern=HIERARCHY_REGEX)]
    """The highest level of namespacing on the broker address, provided by value configured by registry service administrator. Important for connecting different INTERSECT systems."""
    service_name: str
    """The service namespacing of these credentials, reserved by user on registry service."""
    brokers: Annotated[list[ControlPlaneConfig], Field(min_length=1)]
    """List of control plane configurations the SDK should use."""
    data_stores: Annotated[DataStoreConfigMap, Field(default_factory=lambda: DataStoreConfigMap())]
    """List of data plane configurations the SDK should use."""
