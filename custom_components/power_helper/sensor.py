from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.const import UnitOfPower

from .const import DOMAIN

# =====================================================================
# HELPERS
# =====================================================================

def entity_ids(source: str | list[str] | None) -> list[str]:
    """Return one or multiple configured entity IDs as a list."""
    if not source:
        return []
    return [source] if isinstance(source, str) else source


def power_values_in_watt(
    hass: HomeAssistant, entry: ConfigEntry, source: str | list[str] | None
) -> list[float]:
    """Return each source value in Watt."""
    data = entry.options or entry.data
    invert = source == data.get("akku_leistung") and data.get(
        "akku_leistung_invertiert", False
    )
    values = []

    for entity_id in entity_ids(source):
        try:
            state = hass.states.get(entity_id)
            if state is None or state.state in (None, "unknown", "unavailable"):
                continue

            value = float(state.state)
            unit = state.attributes.get("unit_of_measurement")

            if unit in (UnitOfPower.KILO_WATT, "kW"):
                value *= 1000

            values.append(-value if invert else value)
        except Exception:
            continue

    return values


def power_in_watt(
    hass: HomeAssistant, entry: ConfigEntry, source: str | list[str] | None
) -> float:
    """Return the sum of all source values in Watt."""
    return sum(power_values_in_watt(hass, entry, source))


def split_power_in_watt(
    hass: HomeAssistant,
    entry: ConfigEntry,
    source: str | list[str] | None,
    *,
    positive: bool,
) -> float:
    """Split every source by sign before summing it."""
    values = power_values_in_watt(hass, entry, source)
    return sum(max(value, 0) if positive else max(-value, 0) for value in values)


def sum_pv_power(hass: HomeAssistant, entry: ConfigEntry) -> float:
    """Return the sum of all PV sensors in Watt."""
    data = entry.options or entry.data
    pv_sensors = data.get("pv_leistung")

    if not pv_sensors:
        return 0.0

    # Falls nur ein einzelner Sensor angegeben wurde, in eine Liste packen
    pv_sensors = entity_ids(pv_sensors)

    total = 0.0
    for sensor_id in pv_sensors:
        try:
            state = hass.states.get(sensor_id)
            if state is None or state.state in (None, "unknown", "unavailable"):
                continue

            value = float(state.state)
            unit = state.attributes.get("unit_of_measurement")

            if unit in (UnitOfPower.KILO_WATT, "kW"):
                value *= 1000

            total += value
        except Exception:
            continue

    return total


# =====================================================================
# SETUP
# =====================================================================

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    sensors: list[SensorEntity] = []
    data = entry.options or entry.data

    # ==================== GRID ====================

    if data.get("netz_leistung") and not (data.get("netz_bezug") and data.get("netz_einspeisung")):
        sensors += [
            ProxyPowerSensor(hass, source_entity=data["netz_leistung"], entry=entry, key="netz_leistung"),
            SplitPowerSensor(
                hass,
                source_entity=data["netz_leistung"],
                entry=entry,
                key="netz_bezug",
                positive=True,
            ),
            SplitPowerSensor(
                hass,
                source_entity=data["netz_leistung"],
                entry=entry,
                key="netz_einspeisung",
                positive=False,
            ),
        ]

    if not data.get("netz_leistung") and (data.get("netz_bezug") and data.get("netz_einspeisung")):
        sensors += [
            ProxyPowerSensor(hass, source_entity=data["netz_bezug"], entry=entry, key="netz_bezug"),
            ProxyPowerSensor(hass, source_entity=data["netz_einspeisung"], entry=entry, key="netz_einspeisung"),
            CombinedPowerSensor(
                hass,
                pos_entity=data["netz_bezug"],
                neg_entity=data["netz_einspeisung"],
                entry=entry,
                key="netz_leistung",
                ena_def=True,
            ),
        ]

    # ==================== BATTERY ====================

    if data.get("akku_leistung") and not (data.get("akku_laden") and data.get("akku_entladen")):
        sensors += [
            ProxyPowerSensor(hass, source_entity=data["akku_leistung"], entry=entry, key="akku_leistung"),
            InvertedPowerSensor(hass, source_entity=data["akku_leistung"], entry=entry, key="akku_leistung_inv"),
            SplitPowerSensor(
                hass,
                source_entity=data["akku_leistung"],
                entry=entry,
                key="akku_entladen",
                positive=True,
            ),
            SplitPowerSensor(
                hass,
                source_entity=data["akku_leistung"],
                entry=entry,
                key="akku_laden",
                positive=False,
            ),
        ]

    if not data.get("akku_leistung") and (data.get("akku_laden") and data.get("akku_entladen")):
        sensors += [
            ProxyPowerSensor(hass, source_entity=data["akku_laden"], entry=entry, key="akku_laden"),
            ProxyPowerSensor(hass, source_entity=data["akku_entladen"], entry=entry, key="akku_entladen"),
            CombinedPowerSensor(
                hass,
                pos_entity=data["akku_entladen"],
                neg_entity=data["akku_laden"],
                entry=entry,
                key="akku_leistung",
                ena_def=True
            ),
            CombinedPowerSensor(
                hass,
                pos_entity=data["akku_laden"],
                neg_entity=data["akku_entladen"],
                entry=entry,
                key="akku_leistung_inv",
                ena_def=False
            ),
        ]

    # ==================== FLOWS ====================

    flows = {
        "netz": data.get("netz_leistung"),
        "akku": data.get("akku_leistung"),
        "netz_bezug": data.get("netz_bezug"),
        "netz_einspeisung": data.get("netz_einspeisung"),
        "akku_laden": data.get("akku_laden"),
        "akku_entladen": data.get("akku_entladen"),
    }

    sensors.append(FlowPowerSensor(hass, entry, "haus", flows))

    if data.get("pv_leistung"):
        sensors.append(ProxyPvSumPowerSensor(hass, entry=entry, key="pv_leistung"))
        sensors.append(FlowPowerSensor(hass, entry, "pv_zu_haus", flows))
        sensors.append(FlowPowerSensor(hass, entry, "pv_zu_netz", flows))

        if data.get("akku_leistung") or (data.get("akku_laden") and data.get("akku_entladen")):
            sensors.append(FlowPowerSensor(hass, entry, "pv_zu_akku", flows))

    sensors.append(FlowPowerSensor(hass, entry, "netz_zu_haus", flows))

    if data.get("akku_leistung") or (data.get("akku_laden") and data.get("akku_entladen")):
        sensors.append(FlowPowerSensor(hass, entry, "netz_zu_akku", flows))
        sensors.append(FlowPowerSensor(hass, entry, "akku_zu_haus", flows))
        sensors.append(FlowPowerSensor(hass, entry, "akku_zu_netz", flows))

    async_add_entities(sensors)


# =====================================================================
# BASE
# =====================================================================

class BasePhSensor(SensorEntity):
    _attr_should_poll = False
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_icon = "mdi:lightning-bolt-circle"
    _attr_has_entity_name = True

    def __init__(self, *, entry: ConfigEntry, key: str):
        self._entry = entry
        self._attr_translation_key = key
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Dennis90BW",
            model="powerHELPER",
            sw_version="1.0.7",
        )


# =====================================================================
# PROXY
# =====================================================================

class ProxyPowerSensor(BasePhSensor):
    def __init__(self, hass, *, source_entity, entry, key):
        super().__init__(entry=entry, key=key)
        self.hass = hass
        self._source = source_entity
        self._attr_entity_registry_enabled_default = False
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_added_to_hass(self):
        async_track_state_change_event(self.hass, entity_ids(self._source), self._changed)
        self._update()

    @callback
    def _changed(self, event):
        self._update()

    def _update(self):
        self._attr_native_value = power_in_watt(self.hass, self._entry, self._source)
        self.async_write_ha_state()

class ProxyPvSumPowerSensor(BasePhSensor):
    def __init__(self, hass, *, entry, key):
        super().__init__(entry=entry, key=key)
        self.hass = hass
        self._attr_entity_registry_enabled_default = False
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_added_to_hass(self):
        data = self._entry.options or self._entry.data
        pv_sensors = data.get("pv_leistung") or []
        pv_sensors = entity_ids(pv_sensors)

        async_track_state_change_event(self.hass, pv_sensors, self._update)
        self._update()

    @callback
    def _update(self, event=None):
        self._attr_native_value = sum_pv_power(self.hass, self._entry)
        self.async_write_ha_state()

class InvertedPowerSensor(BasePhSensor):
    def __init__(self, hass, *, source_entity, entry, key):
        super().__init__(entry=entry, key=key)
        self.hass = hass
        self._source = source_entity
        self._attr_entity_registry_enabled_default = False

    async def async_added_to_hass(self):
        async_track_state_change_event(self.hass, entity_ids(self._source), self._changed)
        self._update()

    @callback
    def _changed(self, event):
        self._update()

    def _update(self):
        value = power_in_watt(self.hass, self._entry, self._source)
        self._attr_native_value = -value
        self.async_write_ha_state()

# =====================================================================
# SPLIT / COMBINE
# =====================================================================

class SplitPowerSensor(BasePhSensor):
    def __init__(self, hass, *, source_entity, entry, key, positive):
        super().__init__(entry=entry, key=key)
        self.hass = hass
        self._source = source_entity
        self._positive = positive

    async def async_added_to_hass(self):
        async_track_state_change_event(self.hass, entity_ids(self._source), self._changed)
        self._update()

    @callback
    def _changed(self, event):
        self._update()

    def _update(self):
        self._attr_native_value = split_power_in_watt(
            self.hass, self._entry, self._source, positive=self._positive
        )
        self.async_write_ha_state()


class CombinedPowerSensor(BasePhSensor):
    def __init__(self, hass, *, pos_entity, neg_entity, entry, key, ena_def):
        super().__init__(entry=entry, key=key)
        self.hass = hass
        self._pos = pos_entity
        self._neg = neg_entity
        self._attr_entity_registry_enabled_default = ena_def

    async def async_added_to_hass(self):
        async_track_state_change_event(
            self.hass, entity_ids(self._pos) + entity_ids(self._neg), self._changed
        )
        self._update()

    @callback
    def _changed(self, event):
        self._update()

    def _update(self):
        pos = power_in_watt(self.hass, self._entry, self._pos)
        neg = power_in_watt(self.hass, self._entry, self._neg)
        self._attr_native_value = pos - neg
        self.async_write_ha_state()


# =====================================================================
# FLOW SENSORS
# =====================================================================

class FlowPowerSensor(BasePhSensor):
    def __init__(self, hass, entry, key, sources):
        super().__init__(entry=entry, key=key)
        self.hass = hass
        self._key = key
        self._sources = sources

    async def async_added_to_hass(self):
        async_track_state_change_event(
            self.hass,
            [
                entity_id
                for source in self._sources.values()
                for entity_id in entity_ids(source)
            ],
            self._update,
        )
        self._update()

    @callback
    def _update(self, event=None):
        def val(e):
            return power_in_watt(self.hass, self._entry, e) if e else 0.0
        cfg = self._entry.options or self._entry.data
        akku_prio = cfg.get("akku_prio", False)
        netz = val(self._sources["netz"])
        pv = sum_pv_power(self.hass, self._entry)
        akku = val(self._sources["akku"])
        nb = val(self._sources["netz_bezug"])
        ne = val(self._sources["netz_einspeisung"])
        al = val(self._sources["akku_laden"])
        ae = val(self._sources["akku_entladen"])

        if netz != 0 and nb == 0 and ne == 0:
            nb = max(netz, 0)
            ne = max(-netz, 0)

        if netz == 0 and (nb != 0 or ne != 0):
            netz = nb - ne

        if self._sources["akku"] and not (
            self._sources["akku_laden"] and self._sources["akku_entladen"]
        ):
            ae = split_power_in_watt(
                self.hass, self._entry, self._sources["akku"], positive=True
            )
            al = split_power_in_watt(
                self.hass, self._entry, self._sources["akku"], positive=False
            )

        if akku == 0 and (al != 0 or ae != 0):
            akku = ae - al

        haus = netz + pv + akku

        if akku_prio:
            pv_zu_akku = max(min(pv, al),0)
            pv_zu_haus = max(min(max(pv - pv_zu_akku, 0), haus),0)
        else:
            pv_zu_haus = max(min(pv, haus),0)
            pv_zu_akku = max(min(max(pv - pv_zu_haus, 0), al),0)

        pv_zu_netz = max(pv - pv_zu_haus - pv_zu_akku, 0)

        akku_zu_haus = max(min(ae, haus - pv_zu_haus),0)
        akku_zu_netz = max(ae - akku_zu_haus, 0)

        netz_zu_haus = max(haus - pv_zu_haus - akku_zu_haus, 0)
        netz_zu_akku = max(al - pv_zu_akku, 0)

        mapping = {
            "haus": haus,
            "pv_zu_haus": pv_zu_haus,
            "pv_zu_akku": pv_zu_akku,
            "pv_zu_netz": pv_zu_netz,
            "netz_zu_haus": netz_zu_haus,
            "netz_zu_akku": netz_zu_akku,
            "akku_zu_haus": akku_zu_haus,
            "akku_zu_netz": akku_zu_netz,
        }

        self._attr_native_value = mapping.get(self._key, 0)
        self.async_write_ha_state()
