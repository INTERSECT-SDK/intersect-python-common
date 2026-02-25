# INTERSECT common libraries

This library is meant to provide common definitions across all INTERSECT services, both domain science microservices and INTERSECT core services.

## IMPORTANT - READ THIS SECTION

If you are developing a domain science application, do NOT import directly from this package. Use the [intersect-sdk](https://github.com/INTERSECT-SDK/python-sdk) package instead. You also don't need to import this package directly, the `intersect-sdk` package will automatically manage this version for you.

## Version release policy

Note that this package does _not_ follow semantic versioning for everything, as this is meant to be an internal package used by both the INTERSECT SDK and INTERSECT core services; it ONLY follows semantic versioning for the internal message structure.

Prior to release 1.0.0, the policy is:

- MINOR VERSION CHANGE - if the message structure changes (relevant to end users and the ecosystem)
- PATCH VERSION CHANGE - any release, which may or may not be breaking (only relevant to the INTERSECT-SDK and INTERSECT core services)

After release 1.0.0, the policy is expected to be:

- MAJOR VERSION CHANGE - if the message structure changes (relevant to end users and the ecosystem)
- MINOR VERSION CHANGE - breaking API changes (this is only relevant to the INTERSECT-SDK and INTERSECT core services)
- PATCH VERSION CHANGE - backwards compatible changes

The INTERSECT-SDK MUST follow semantic versioning, and MUST update its semantic version if this package's semantic version is updated.

## Developing

```bash
uv venv .venv
source .venv/bin/activate
uv sync --locked --all-extras --dev
```
