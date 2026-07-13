# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.4] - 2026-07-12

### Fixed

- Prevent post-command cloud polls from reverting switch/light state when Pepper OS returns stale `power_on` (fixes automations appearing to fail after optimistic updates).

## [0.4.3] - 2026-05-27

### Added

- **Restart** button entity per switch/light device (`PUT .../command/Restart/`), with API docs noting fast reboots may not appear as unavailable during 30s polling.

## [0.4.2] - 2026-05-27

### Added

- Device firmware version (`sw_version` in Home Assistant) from Pepper `firmware.version`.
- Wi-Fi network name, timezone, last paired time, cloud status, and external device id from `GET /account/devices/`.
- Entity attributes and config-entry storage for the new metadata; CLI test tool prints the extra fields.
- API docs for the additional device payload fields.

## [0.4.1] - 2026-05-27

### Changed

- Switch and light entities update instantly when toggled (optimistic coordinator state) instead of waiting for a full cloud poll.

## [0.4.0] - 2026-05-27

### Added

- Centered logo and badges on the README.
- Credits for PCAPdroid, apk-mitm, mitmproxy, logcat, Pepper SDK, httpx, Home Assistant, and HACS.
- GitHub Releases workflow; `manifest.json` version must match release tags for HACS and Home Assistant Updates.

### Changed

- HACS is the recommended install path; manual install points to the latest GitHub Release.

## [0.3.9] - 2026-05-26

### Added

- Repository-root `brand/` assets for HACS validation.

## [0.3.8] - 2026-05-26

### Changed

- Removed cloud account hub device; plugs appear as standalone devices under the integration.
- Cleans up legacy self-referential device registry links on setup.

## [0.3.7] - 2026-05-26

### Fixed

- Options re-sync no longer crashes with `TypeError: a coroutine was expected` (async reload listener).
- Restored `powerStateOn` with `valueJson` toggling (reverted `powerStateOff` experiment).

## [0.3.6] - 2026-05-26

### Fixed

- Coordinator reads devices from options re-sync (multi-device support).
- Hub device linking and `powerStateOff` command path (superseded in 0.3.7).

## [0.3.5] - 2026-05-26

### Fixed

- Removed invalid `via_device` self-reference on device entities.
- HTTP client creation moved off the event loop (`asyncio.to_thread`) to avoid HA blocking warnings.

## [0.3.4] - 2026-05-26

### Fixed

- Proactive Pepper session refresh before AWS credentials expire (~15 minutes).
- Retry signed requests on 403 / expired credential errors.
- Single `list_devices()` call per coordinator poll.

## [0.3.3] - 2026-05-26

### Added

- Brand icons under `custom_components/merkury_smart/brand/` for Home Assistant 2026.3+.

## [0.3.2] - 2026-05-26

### Fixed

- Restored httpx/HTTP2 Pepper cloud client (setup failure).

## [0.3.1] - 2026-05-26

### Fixed

- Config flow syntax error.

## [0.1.0] - 2026-05-26

### Added

- Initial Pepper OS cloud integration: login, device discovery, switch/light on-off.

[Unreleased]: https://github.com/AKASGaming/merkury-smart-home-assistant/compare/v0.4.1...HEAD
[0.4.1]: https://github.com/AKASGaming/merkury-smart-home-assistant/releases/tag/v0.4.1
[0.4.0]: https://github.com/AKASGaming/merkury-smart-home-assistant/releases/tag/v0.4.0
