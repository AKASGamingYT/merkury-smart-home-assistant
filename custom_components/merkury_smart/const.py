"""Constants for the Merkury Smart integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "merkury_smart"
PLATFORMS: Final = ["button", "light", "switch"]

# Account
CONF_USERNAME: Final = "username"
CONF_PASSWORD: Final = "password"
CONF_ENVIRONMENT: Final = "environment"
CONF_BRAND: Final = "brand"

CONF_DEVICES: Final = "devices"
CONF_DEVICE_ID: Final = "device_id"
CONF_NAME: Final = "name"
CONF_DEVICE_CLASS: Final = "device_class"
CONF_MODEL: Final = "model"
CONF_DEVICE_TYPE: Final = "device_type"
CONF_PROVIDER: Final = "provider"
CONF_EXTERNAL_DEVICE_ID: Final = "external_device_id"
CONF_FIRMWARE_VERSION: Final = "firmware_version"
CONF_WIFI_NETWORK: Final = "wifi_network"
CONF_TIMEZONE: Final = "timezone"
CONF_LAST_PAIRED_AT: Final = "last_paired_at"
CONF_CLOUD_STATUS: Final = "cloud_status"

DEFAULT_BRAND: Final = "geeni"

DEVICE_CLASS_LIGHT: Final = "light"
DEVICE_CLASS_SWITCH: Final = "switch"

ENVIRONMENTS: Final = {
    "production": "Production (api.pepperos.io)",
    "staging": "Staging",
    "uat": "UAT",
    "dev": "Development",
}

# Pepper device commands (from Merkury Smart app activity types)
CMD_POWER_ON: Final = "powerStateOn"
CMD_POWER_OFF: Final = "powerStateOff"
CMD_RESTART: Final = "Restart"

BRIGHTNESS_MIN: Final = 10
BRIGHTNESS_MAX: Final = 1000

UPDATE_INTERVAL_SECONDS: Final = 30

# Ignore polled power_on that disagrees with a recent command (cloud can lag).
POWER_COMMAND_GRACE_SECONDS: Final = 10
