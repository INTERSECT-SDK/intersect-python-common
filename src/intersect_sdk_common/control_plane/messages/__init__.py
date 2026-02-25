"""This package describes the structure of the headers associated with all messages sent over the wire.

It does not necessarily describe the structure of the message body, as this is determined by a combination of the schema and parsing the message headers.

Because services/clients must define their own callback functions, they are responsible for determining what type of message headers they are expecting in the callback.
"""
