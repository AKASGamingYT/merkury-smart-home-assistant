"""Data update coordinator for Merkury Smart devices."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .cloud import MerkuryCloudClient
from .const import CONF_DEVICE_ID, DOMAIN, POWER_COMMAND_GRACE_SECONDS, UPDATE_INTERVAL_SECONDS
from .helpers import get_entry_devices

_LOGGER = logging.getLogger(__name__)


class MerkuryCoordinator(DataUpdateCoordinator[dict[str, dict]]):
    """Poll Merkury Smart devices via the Pepper OS cloud API."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: MerkuryCloudClient,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )
        self.entry = entry
        self.client = client
        self._pending_power: dict[str, tuple[bool, float]] = {}

    def _configured_device_ids(self) -> list[str]:
        return [device[CONF_DEVICE_ID] for device in get_entry_devices(self.entry)]

    async def _async_update_data(self) -> dict[str, dict]:
        device_ids = self._configured_device_ids()
        try:
            polled = await self.client.poll_device_states(device_ids)
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Update failed: %s", err)
            raise UpdateFailed(str(err)) from err
        return self._merge_polled_states(polled)

    def _merge_polled_states(self, polled: dict[str, dict]) -> dict[str, dict]:
        """Apply poll results while preserving recent local power commands."""

        if not self._pending_power:
            return polled

        now = self.hass.loop.time()
        merged: dict[str, dict] = {}
        for device_id, state in polled.items():
            merged[device_id] = dict(state)
            pending = self._pending_power.get(device_id)
            if pending is None:
                continue

            expected_on, commanded_at = pending
            age = now - commanded_at
            polled_on = state.get("power_on")

            if age > POWER_COMMAND_GRACE_SECONDS:
                self._pending_power.pop(device_id, None)
                continue

            if polled_on == expected_on:
                self._pending_power.pop(device_id, None)
                continue

            merged[device_id]["power_on"] = expected_on
            _LOGGER.debug(
                "Keeping commanded power_on=%s for %s (poll had %s, age=%.1fs)",
                expected_on,
                device_id,
                polled_on,
                age,
            )

        return merged

    @callback
    def _apply_power_state(self, device_id: str, on: bool) -> None:
        """Push a power state change to coordinator data and refresh entities."""

        data = dict(self.data or {})
        state = dict(data.get(device_id, {}))
        state["power_on"] = on
        data[device_id] = state
        self.async_set_updated_data(data)

    async def set_power(self, device_id: str, on: bool) -> None:
        """Set device power with optimistic UI update, then reconcile via cloud."""

        _LOGGER.debug("set_power device_id=%s on=%s", device_id, on)
        previous_state = (
            dict(self.data[device_id]) if self.data and device_id in self.data else {}
        )

        self._pending_power[device_id] = (on, self.hass.loop.time())
        self._apply_power_state(device_id, on)
        try:
            await self.client.set_power(device_id, on)
        except Exception:
            _LOGGER.exception("set_power failed for %s", device_id)
            self._pending_power.pop(device_id, None)
            data = dict(self.data or {})
            data[device_id] = previous_state
            self.async_set_updated_data(data)
            raise

        # Reconcile other fields from cloud without clobbering commanded power_on.
        self.hass.async_create_task(self.async_request_refresh())

    async def restart_device(self, device_id: str) -> bool:
        """Send cloud restart command. Does not change coordinator state (see docs)."""

        _LOGGER.debug("restart_device device_id=%s", device_id)
        try:
            accepted = await self.client.restart_device(device_id)
        except Exception:
            _LOGGER.exception("restart_device failed for %s", device_id)
            raise
        self.hass.async_create_task(self.async_request_refresh())
        return accepted

    async def async_shutdown(self) -> None:
        await self.client.close()
