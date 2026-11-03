<p align="center">
  <img
    src="https://raw.githubusercontent.com/AKASGamingYT/merkury-smart-home-assistant/main/brand/icon.png"
    alt="Merkury Smart"
    width="220"
  />
</p>

<h1 align="center">Merkury Smart for Home Assistant</h1>

<p align="center">
  <a href="https://github.com/AKASGamingYT/merkury-smart-home-assistant/releases">
    <img src="https://img.shields.io/github/v/release/AKASGamingYT/merkury-smart-home-assistant?label=release" alt="Latest release" />
  </a>
  <a href="https://github.com/AKASGamingYT/merkury-smart-home-assistant/stargazers">
    <img src="https://img.shields.io/github/stars/AKASGamingYT/merkury-smart-home-assistant?style=social" alt="GitHub stars" />
  </a>
</p>

<p align="center">
  Home Assistant custom integration for <strong><a href="https://www.merkurysmart.com/">Merkury Smart</a></strong> devices — the app-backed cloud path that works for current Merkury accounts.
</p>

<p align="center">
  Powered by the <a href="https://pepperos.io">Pepper OS</a> cloud (<code>api.pepperos.io</code>) — same backend as <strong>Geeni</strong> and other Pepper brands.
</p>

---

## Why this exists

Merkury plugs and bulbs use Tuya chipsets, but **Merkury Smart app accounts live on Pepper OS**, not Smart Life or the Tuya IoT developer platform. The official [Tuya](https://www.home-assistant.io/integrations/tuya/) integration and [Xtend Tuya](https://github.com/azerty9971/xtend_tuya) often show **no devices** for Merkury-only users.

This integration logs in the same way the Merkury Smart Android app does — email/password to Pepper OS, AWS SigV4 signed requests over HTTP/2. No APK key extraction or Tuya developer account required.

| Approach | Merkury Smart app accounts | Notes |
| -------- | -------------------------- | ----- |
| Official Tuya + Xtend Tuya | Usually **no** | Needs Smart Life linking |
| **This integration** | **Yes** | Pepper OS; Merkury Smart + Geeni + other Pepper brands |
| Tuya CloudCutter + ESPHome | Yes | Permanent; breaks Merkury app control |

## Tested hardware

Verified against a live Merkury Smart account:

| Device | Model | Control |
| ------ | ----- | ------- |
| Smart plug | **MI-WW134-199W-B** | On/off via cloud `powerStateOn` |

Other Merkury / Geeni plugs, bulbs, and strips on the same Pepper cloud should discover automatically if they appear in the Merkury Smart app. Brightness/color control is planned; on/off works today for switches.

## Install in Home Assistant

Requires **Home Assistant 2024.1+** (brand icons in the UI need **2026.3+** — see [docs/BRANDING.md](docs/BRANDING.md)).

### Option A — HACS (recommended)

1. HACS → Integrations → ⋮ → **Custom repositories**
2. Add `https://github.com/AKASGamingYT/merkury-smart-home-assistant` as type **Integration**
3. Search **Merkury Smart**, install, and **restart Home Assistant**
4. Settings → Devices & Services → **Add Integration** → **Merkury Smart**
5. Sign in with your **Merkury Smart email and password** (same as the app)
6. Leave **brand** as **`geeni`** (required for Merkury Smart accounts on Pepper OS)
7. Choose **Production** for the cloud environment

HACS uses [GitHub Releases](https://github.com/AKASGamingYT/merkury-smart-home-assistant/releases) for version numbers. The release tag (e.g. `v0.4.0`) matches `version` in `custom_components/merkury_smart/manifest.json` (without the `v` prefix), which is what Home Assistant shows under **Settings → Updates**.

### Option B — Manual copy

1. **Download** the [latest release](https://github.com/AKASGamingYT/merkury-smart-home-assistant/releases/latest) or clone this repository:
   ```bash
   git clone https://github.com/AKASGamingYT/merkury-smart-home-assistant.git
   ```
2. Copy the integration folder into your Home Assistant config:
   ```text
   config/custom_components/merkury_smart/
   ```
   Include `__init__.py`, `manifest.json`, `brand/`, `pepper_cloud/`, and the rest of the package.
3. **Restart Home Assistant**, then add the integration as in steps 4–7 above.

Home Assistant installs `httpx[http2]` automatically from `manifest.json` on first load.

**Icons:** If the Merkury icon appears under **Integrations** but not in the HACS store or **Updates** list, your install is fine — see [docs/BRANDING.md](docs/BRANDING.md).

### After setup

- Devices from your Merkury Smart account appear as **switch** (plugs) or **light** entities, plus a **Restart** button per device (cloud command; see [docs/PEPPER_CLOUD_API.md](docs/PEPPER_CLOUD_API.md)).
- Use **Configure → Re-sync devices** on the integration card to refresh the device list.
- Poll interval defaults to cloud polling (about 30s). Fast plug reboots often finish before the next poll, so the Restart button may not show a brief `unavailable` state in Home Assistant.

## Command-line test (optional)

Validate login and device discovery before touching Home Assistant:

```powershell
python -m pip install "httpx[http2]"
python tools/test_pepper_cloud.py --email you@example.com --password "your-password"
```

Add `--diagnose` to print signed-request probes to stderr.

## Supported device types

| Type | Examples | Control today |
| ---- | -------- | ------------- |
| Smart plug | MI-WW134-199W-B, MI-WW334, MI-WW102 | On/off, Restart button |
| Bulbs / strips | Merkury / Geeni lights | On/off, Restart button (brightness read; dimming planned) |

Anything listed in the Merkury Smart or Geeni app under the same account should be discoverable via `GET /account/devices/`.

## Technical notes

- **Cloud:** Pepper OS `api.pepperos.io` (production)
- **Auth:** `POST /authentication/byEmail` → JWT `peppertoken` + temporary AWS credentials
- **Transport:** HTTP/2 required for signed routes (large auth headers); uses `httpx`
- **Control:** `PUT /account/devices/{id}/settings/powerStateOn/` with `{"valueJson":"1"|"0"}`; optional `PUT .../command/Restart/` (Restart button)

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/PEPPER_CLOUD_API.md](docs/PEPPER_CLOUD_API.md).

## Releases and versioning

| What | Where |
| ---- | ----- |
| Human-facing version | [GitHub Releases](https://github.com/AKASGamingYT/merkury-smart-home-assistant/releases) (`v0.4.0`, …) |
| Home Assistant / HACS | `custom_components/merkury_smart/manifest.json` → `"version": "0.4.0"` (no `v`) |
| Updates card in HA | Shown when HACS is installed and a newer **release** exists |

New versions are published as **GitHub Releases** (not tags alone). Pushing a tag matching `manifest.json` triggers the [release workflow](.github/workflows/release.yml), which publishes the matching section from [CHANGELOG.md](CHANGELOG.md) as the release notes.

**Releasing a new version:** update `CHANGELOG.md` (move notes from `[Unreleased]` into `## [x.y.z] - date`), bump `manifest.json`, commit, then `git tag vX.Y.Z` and `git push origin main --tags`.

## Project status

| Phase | Goal | Status |
| ----- | ---- | ------ |
| 0 | Architecture & docs | Done |
| 1 | Pepper OS login + discovery | Done |
| 2 | Cloud switch/light entities | Done |
| 3 | Brightness/color via settings API | Planned |
| 4 | Local LAN fallback | Research |

## Credits and acknowledgements

This integration was reverse-engineered from the **Merkury Smart** Android app (`com.merkury.geeni`) and the public **Pepper OS** API. Thanks to the projects and communities that made that possible:

| Project | Role |
| ------- | ---- |
| [PCAPdroid](https://github.com/emanuele-f/PCAPdroid) | On-device traffic capture; TLS export for API discovery |
| [apk-mitm](https://github.com/shroudedcode/apk-mitm) | Patching the Merkury Smart APK for HTTPS inspection |
| [mitmproxy](https://mitmproxy.org/) | Decrypting and documenting `api.pepperos.io` requests |
| Android **logcat** | Login flow ordering (`byToken` before signed routes) |
| Decompiled **Pepper SDK** (Merkury Smart APK) | Endpoint paths, models, and SigV4 signing behavior |
| [httpx](https://www.python-httpx.org/) / [h2](https://github.com/python-hyper/h2) | HTTP/2 client used by the integration |
| [Home Assistant](https://www.home-assistant.io/) | Platform and [custom integration](https://developers.home-assistant.io/docs/creating_integration_file_structure/) APIs |
| [HACS](https://hacs.xyz/) | Distribution and update discovery via GitHub Releases |

Related integrations that informed the approach: [eufy_security](https://github.com/fuatakgun/eufy_security) (app-style cloud mimic) and community Tuya/Pepper research threads.

## License

MIT — see [LICENSE](LICENSE).
