import pytest
from pydantic import TypeAdapter, ValidationError

from intersect_sdk_common.config import (
    ControlPlaneConfig,
    DataStoreConfig,
    IntersectConfig,
)

# TESTS #####################

# NOTE: with dataclasses, need to validate dictionaries instead of the dataclass directly


def test_missing_control_plane_config():
    with pytest.raises(ValidationError) as ex:
        TypeAdapter(ControlPlaneConfig).validate_python({})
    errors = [{'type': e['type'], 'loc': e['loc']} for e in ex.value.errors()]
    assert len(errors) == 3
    assert {'type': 'missing', 'loc': ('username',)} in errors
    assert {'type': 'missing', 'loc': ('password',)} in errors
    assert {'type': 'missing', 'loc': ('protocol',)} in errors


def test_invalid_control_plane_config():
    with pytest.raises(ValidationError) as ex:
        TypeAdapter(ControlPlaneConfig).validate_python(
            ControlPlaneConfig(
                host='',
                username='',
                password='',
                port=0,
                protocol='mqtt',  # type: ignore[arg-type]
            ).__dict__
        )
    errors = [{'type': e['type'], 'loc': e['loc']} for e in ex.value.errors()]
    assert len(errors) == 5
    assert {'type': 'string_too_short', 'loc': ('username',)} in errors
    assert {'type': 'string_too_short', 'loc': ('password',)} in errors
    assert {'type': 'string_too_short', 'loc': ('host',)} in errors
    assert {'type': 'greater_than', 'loc': ('port',)} in errors
    assert {'type': 'literal_error', 'loc': ('protocol',)} in errors


def test_missing_data_plane_config():
    with pytest.raises(ValidationError) as ex:
        TypeAdapter(DataStoreConfig).validate_python({})
    errors = [{'type': e['type'], 'loc': e['loc']} for e in ex.value.errors()]
    assert len(errors) == 2
    assert {'type': 'missing', 'loc': ('username',)} in errors
    assert {'type': 'missing', 'loc': ('password',)} in errors


def test_invalid_data_plane_config():
    with pytest.raises(ValidationError) as ex:
        TypeAdapter(DataStoreConfig).validate_python(
            DataStoreConfig(
                host='',
                username='',
                password='',
                port=0,
            ).__dict__
        )
    errors = [{'type': e['type'], 'loc': e['loc']} for e in ex.value.errors()]
    assert len(errors) == 4
    assert {'type': 'string_too_short', 'loc': ('username',)} in errors
    assert {'type': 'string_too_short', 'loc': ('password',)} in errors
    assert {'type': 'string_too_short', 'loc': ('host',)} in errors
    assert {'type': 'greater_than', 'loc': ('port',)} in errors


def test_missing_intersect_config():
    with pytest.raises(ValidationError) as ex:
        TypeAdapter(IntersectConfig).validate_python({})
    errors = [{'type': e['type'], 'loc': e['loc']} for e in ex.value.errors()]
    assert len(errors) == 3
    assert {'type': 'missing', 'loc': ('brokers',)} in errors
    assert {'type': 'missing', 'loc': ('system_name',)} in errors
    assert {'type': 'missing', 'loc': ('service_name',)} in errors


def test_invalid_intersect_config():
    with pytest.raises(ValidationError) as ex:
        TypeAdapter(IntersectConfig).validate_python(
            IntersectConfig(
                system_name='I AM INVALID',
                service_name=7,
                brokers=[],
            ).__dict__
        )
    errors = [{'type': e['type'], 'loc': e['loc']} for e in ex.value.errors()]
    assert len(errors) == 3
    assert {'type': 'string_pattern_mismatch', 'loc': ('system_name',)} in errors
    assert {'type': 'string_type', 'loc': ('service_name',)} in errors
    assert {'type': 'too_short', 'loc': ('brokers',)} in errors
