import pytest

from intersect_sdk_common.control_plane.custom_binary_protocol import (
    CONTENT_TYPE_HEADER_KEY,
    create_binary_message,
    parse_binary_message,
)


@pytest.mark.parametrize(
    ('body', 'content_type', 'headers'),
    [
        (b'{"key": "value"}', 'application/json', {'header1': 'value1', 'header2': 'value2'}),
        (b'<xml><key>value</key></xml>', 'application/xml', {'header1': 'value1'}),
        (b'plain text body', 'text/plain', {}),
        (
            b'I\x01Have\x02Special\x03Characters',
            'text/plain',
            {'But headers': 'cannot have control characters'},
        ),
    ],
)
def test_custom_binary_protocol_idempotency(
    body: bytes, content_type: str, headers: dict[str, str]
):
    message = create_binary_message(body, content_type, headers)
    parsed_body, parsed_content_type, parsed_headers = parse_binary_message(message)

    assert parsed_body == body
    assert parsed_content_type == content_type
    assert parsed_headers == headers

    # message body should be at the end of the full message
    body_len = len(body)
    assert body == message[-body_len:]

    # complete message should only add 2 bytes for each metadata field
    assert (
        len(body)
        + len(CONTENT_TYPE_HEADER_KEY)
        + len(content_type)
        + 2  # header key separator and header value terminator
        + sum(
            len(key) + len(value) + 2  # header key separator and header value terminator
            for key, value in headers.items()
        )
        == len(message)
    )
