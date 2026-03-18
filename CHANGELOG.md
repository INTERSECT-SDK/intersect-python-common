# Changelog

We follow [Common Changelog](https://common-changelog.org/) formatting for this document.

## [0.9.3] - 2026-03-18

No API changes.

### Fixed

- Correct wildcard handling within ControlPlaneManager ([commit](https://github.com/INTERSECT-SDK/intersect-python-common/commit/c681856214d329874fa51f7c50b346a66825e5c5)) (Lance Drane)

## [0.9.2] - 2026-03-17

No API changes.

### Fixed

- Made support for wildcards in the channel parameter of `ControlPlaneManager.add_subscription_channel()` consistent across protocols ([commit](https://github.com/INTERSECT-SDK/intersect-python-common/commit/70b90373923e044f5e3059a22c48379a86f7fcc8)) (Lance Drane)

## [0.9.1] - 2026-02-25

Initial reorganization of SDK packaging.

### Changed

- Added new argument to `ControlPlaneManager.add_subscription_channel()` which specifies a queue name to use.
- Add `is_root` option to `ControlPlaneConfig` in preparation for Registry Service.

[0.9.2]: https://github.com/INTERSECT-SDK/intersect-python-common/releases/tag/0.9.2
[0.9.1]: https://github.com/INTERSECT-SDK/intersect-python-common/releases/tag/0.9.1
