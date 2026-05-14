# ⚡ powerHELPER
**a little Home Assistant integration for power flows**

[![HACS Badge](https://img.shields.io/badge/HACS-custom-orange?style=flat-square&logo=homeassistantcommunitystore&logoColor=white)](https://hacs.xyz)
[![GitHub Release](https://img.shields.io/github/v/release/Dennis90BW/ha-power-helper?style=flat-square&logo=github)](https://github.com/Dennis90BW/ha-power-helper/releases)
[![GitHub License](https://img.shields.io/github/license/Dennis90BW/ha-power-helper?style=flat-square)](https://github.com/Dennis90BW/ha-power-helper?tab=MIT-1-ov-file)
[![Installs Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.power_helper.total&suffix=%20installs&style=flat-square&logo=home-assistant&logoColor=white&label=usage)](https://analytics.home-assistant.io/)
[![Code size](https://img.shields.io/github/languages/code-size/Dennis90BW/ha-power-helper?style=flat-square&logo=python&logoColor=white)](https://github.com/Dennis90BW/ha-power-helper)

🇩🇪 [Deutsch](README_de.md) | 🇺🇸 [English](README.md)

**powerHELPER** is a custom integration for **Home Assistant** that automatically breaks down electrical power flows between the **PV system, grid, battery, and home**.

Ideal for users of [Solar Forecast ML](https://github.com/Zara-Toorox/ha-solar-forecast-ml) and SFML-Stats. Thanks @Zara-Toorox for these awesome integrations!

---

## ⚠️ Disclaimer
This is my first GitHub project, and the custom integration was created with the help of AI. Despite careful implementation, **errors or inaccuracies may occur**. Feedback, [issues](https://github.com/Dennis90BW/ha-power-helper/issues), and improvement suggestions are always welcome!

---

## ✨ Features

- 🧩 Automatically creates missing **combined or separate power sensors** for **grid** and **battery**
- 🔌 Power flow breakdown (PV, grid, battery, home)
- ➕ Multiple PV systems can be added
- 🔋 Battery power can be inverted
- ⚙️ Easy setup and editing via the UI
- 📊 Output in **watts (W)**
- 🔄 Supports sensors in **W** and **kW**
- 🌍 Multilingual (**DE / EN**)

---

## 📦 Requirements

- Home Assistant **2025.12.x or newer**
- Existing power sensors with `device_class: power`:
  - Required: grid power **or** grid consumption & feed-in
  - Optional: PV power
  - Optional: battery power **or** battery charge & discharge

---

## 🚀 Installation

### 🔹 HACS (recommended)

1. Open **HACS**
2. Search for **powerHELPER**
3. Click **Download**
4. Restart Home Assistant

---

### 🔹 Manual Installation

1. Download the repository
2. Copy the `power_helper` folder to: `config/custom_components/`
3. Restart Home Assistant

---

## ⚙️ Configuration

1. **Settings → Devices & Services**
2. **Add Integration**
3. Select **powerHELPER**
4. Set device name
5. Select your power sensors

---

## 🧠 Created Sensors

### 🔌 Grid
#### Input
- `sensor.device_grid_power` — Grid power
- `sensor.device_grid_consumption` — Grid consumption
- `sensor.device_grid_feed_in` — Grid feed-in
#### Power flow
- `sensor.device_grid_to_home` — Grid → Home
- `sensor.device_grid_to_battery` — Grid → Battery

### ☀️ PV
#### Input
- `sensor.device_pv_power` — PV power
#### Power flow
- `sensor.device_pv_to_home` — PV → Home
- `sensor.device_pv_to_battery` — PV → Battery
- `sensor.device_pv_to_grid` — PV → Grid

### 🔋 Battery
#### Input
- `sensor.device_battery_power` — Battery power
- `sensor.device_battery_power_inverted` — Battery power inverted
- `sensor.device_battery_charging` — Battery charging
- `sensor.device_battery_discharging` — Battery discharging
#### Power flow
- `sensor.device_battery_to_home` — Battery → Home
- `sensor.device_battery_to_grid` — Battery → Grid

### 🏠 Home
- `sensor.device_home_power` — Home power

All sensors provide **watts (W)** and are fully dashboard-ready.

---

## ❓ FAQ

### Do I need AC or DC sensors?

In general, all sensors for this balance should be AC power sensors, as they represent the actual power flows in the electrical circuit.

DC sensors, such as those coming directly from inverters in the PV system or certain battery storage systems, can also be used. In this case, the DC/AC conversion losses are simply reflected in the **Home Power**, causing the overall consumption of the home to increase, similar to other electrical consumers.

---

## 🧪 Status

Version: **1.0.7**  

Tested with PV + battery systems

---

## 📄 License

MIT License  

Copyright (c) 2026 Dennis

---
