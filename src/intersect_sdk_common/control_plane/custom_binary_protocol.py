"""This module contains the binary specification for an INTERSECT message IF the protocol does not provide any built-in header support. If it does, use the built-in functionality of the protocol.

Some protocols do not have any built-in header support, leaving it up to us to define the binary structure of the message. We want to avoid "chunking" messages into multiple parts, so a message should be guaranteed to include all metadata.
"""

from intersect_sdk_common import IntersectApplicationError

_HEADER_KV_SEPARATOR = b'\x02'
"""Indicates end of a header key and start of a header value.

Used because applications should generally assign no special meaning to this byte, and this byte has no reason to appear in header keys or values.
"""
_HEADER_VALUE_SEPARATOR = b'\x03'
"""Indicates end of a header value and start of the next header key.

Used because applications should generally assign no special meaning to this byte, and this byte has no reason to appear in header keys or values.
"""
_PAYLOAD_SEPARATOR = b'\x01'
"""Indicates end of headers and start of the payload.

Used because applications should generally assign no special meaning to this byte, and this byte has no reason to appear in header keys or values.
"""

_TOTAL_REASONABLE_HEADER_BYTES = 131072
"""The total number of bytes that should be reasonably expected to be used for header keys, values, and header separators combined. This provides applications with some level of DOS protection.

It is rare in practice for ANY application to use this number of bytes for the total amount of headers, for example http2_max_header_size in NGINX is rarely set above 128KB
"""

CONTENT_TYPE_HEADER_KEY = 'content_type'
CONTENT_TYPE_HEADER_KEY_BYTES = CONTENT_TYPE_HEADER_KEY.encode()


def create_binary_message(body: bytes, content_type: str, headers: dict[str, str]) -> bytes:
    """Create a binary message from the body, headers, and content type."""
    return b''.join(
        [
            # content-type 'header' first (this is generally handled separately from other headers in many protocols)
            CONTENT_TYPE_HEADER_KEY_BYTES,
            _HEADER_KV_SEPARATOR,
            content_type.encode(),
            _HEADER_VALUE_SEPARATOR if len(headers) else b'',
            # headers
            _HEADER_VALUE_SEPARATOR.join(
                _HEADER_KV_SEPARATOR.join([key.encode(), value.encode()])
                for key, value in headers.items()
            ),
            # end of headers
            _PAYLOAD_SEPARATOR,
            # body
            body,
        ]
    )


def parse_binary_message(message: bytes) -> tuple[bytes, str, dict[str, str]]:
    """Parse a binary message into its body, content type, and headers."""
    # IMPORTANT!!! ----- Total length of header keys and values combined should be limited to first several bytes, terminate header search early if headers aren't a reasonable length.
    payload_sep_location = message.find(_PAYLOAD_SEPARATOR, 0, _TOTAL_REASONABLE_HEADER_BYTES)
    if payload_sep_location == -1:
        msg = 'Probable malformed message: no payload separator found in first expected bytes, .'
        raise IntersectApplicationError(msg)
    header_string = message[:payload_sep_location]
    headers = {
        key.decode(): value.decode()
        for key, value in (
            header.split(_HEADER_KV_SEPARATOR)
            for header in header_string.split(_HEADER_VALUE_SEPARATOR)
        )
    }
    try:
        content_type = headers.pop(CONTENT_TYPE_HEADER_KEY)
    except KeyError as e:
        msg = 'Probable malformed message: no content_type header found in message, discarding it.'
        raise IntersectApplicationError(msg) from e

    return message[payload_sep_location + 1 :], content_type, headers
