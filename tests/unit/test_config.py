import pytest
from pydantic import TypeAdapter, ValidationError

from intersect_sdk_common.config import (
    ControlPlaneConfig,
    DataStoreConfig,
    HierarchyConfig,
)

# TESTS #####################


def test_empty_hierarchy():
    with pytest.raises(ValidationError) as ex:
        HierarchyConfig()  # type: ignore[call-arg]
    errors = ex.value.errors()
    assert len(errors) == 4
    assert all(e['type'] == 'missing' for e in errors)
    locations = [e['loc'] for e in errors]
    assert ('organization',) in locations
    assert ('facility',) in locations
    assert ('system',) in locations
    assert ('service',) in locations


def test_invalid_hierarchy():
    with pytest.raises(ValidationError) as ex:
        HierarchyConfig(
            organization='no.periods',
            facility='no_underscores',
            system='',
            subsystem='no/slashes',
            service='a',
        )
    errors = ex.value.errors()
    assert len(errors) == 5
    assert all(e['type'] == 'string_pattern_mismatch' for e in errors)
    locations = [e['loc'] for e in errors]
    assert ('organization',) in locations
    assert ('facility',) in locations
    assert ('system',) in locations
    assert ('subsystem',) in locations
    assert ('service',) in locations


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
