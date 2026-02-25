import intersect_sdk_common


def test_imports() -> None:
    """Quick PEP-562 test, make sure every import is valid."""
    for attr in dir(intersect_sdk_common):
        assert getattr(intersect_sdk_common, attr) is not None
