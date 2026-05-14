# ⚡ powerHELPER
**a little Home Assistant integration for power flows**

[![HACS Badge](https://img.shields.io/badge/HACS-custom-orange?style=flat-square&logo=homeassistantcommunitystore&logoColor=white)](https://hacs.xyz)
[![GitHub Release](https://img.shields.io/github/v/release/Dennis90BW/ha-power-helper?style=flat-square&logo=github)](https://github.com/Dennis90BW/ha-power-helper/releases)
[![GitHub License](https://img.shields.io/github/license/Dennis90BW/ha-power-helper?style=flat-square)](https://github.com/Dennis90BW/ha-power-helper?tab=MIT-1-ov-file)
[![Installs Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.power_helper.total&suffix=%20installs&style=flat-square&logo=home-assistant&logoColor=white&label=usage)](https://analytics.home-assistant.io/)
[![Code size](https://img.shields.io/github/languages/code-size/Dennis90BW/ha-power-helper?style=flat-square&logo=python&logoColor=white)](https://github.com/Dennis90BW/ha-power-helper)

🇩🇪 [Deutsch](README_de.md) | 🇺🇸 [English](README.md)

**powerHELPER** ist eine Custom Integration für **Home Assistant**, mit der elektrische Leistungsflüsse zwischen **PV-Anlage, Netz, Akku und Haus** automatisch aufgeschlüsselt werden.

Ideal für Nutzer von [Solar Forecast ML](https://github.com/Zara-Toorox/ha-solar-forecast-ml) und SFML-Stats. Danke @Zara-Toorox für diese tollen Integrationen!

---

## ⚠️ Disclaimer
Dies ist mein erstes GitHub-Projekt und die Custom Integration wurde mithilfe von KI erstellt. Trotz sorgfältiger Umsetzung **können Fehler oder Ungenauigkeiten auftreten**. Feedback, [Issues](https://github.com/Dennis90BW/ha-power-helper/issues) und Verbesserungsvorschläge sind jederzeit willkommen!

---

## ✨ Features

- 🧩 Erstellt automatisch fehlende **kombinierte oder getrennte Leistungssensoren** für **Netz-** und **Akkuleistung**
- 🔌 Aufteilung von Leistungsflüssen (PV, Netz, Akku, Haus)
- 🔋 Akku-Leistung kann invertiert werden
- ➕ Mehrere PV-Anlagen können hinzugefügt werden
- ⚙️ Einfache Einrichtung und Bearbeitung über die UI
- 📊 Ausgabe in **Watt (W)**
- 🔄 Unterstützt Sensoren in **W** und **kW**
- 🌍 Mehrsprachig (DE / EN)

---

## 📦 Voraussetzungen

- Home Assistant **2025.12.x oder neuer**
- Vorhandene Leistungssensoren mit device_class "power":
  - Pflicht: Netz Leistung **oder** Netzbezug & Einspeisung
  - Optional: PV-Leistung
  - Optional: Akku Leistung **oder** Akku Laden & Entladen

---

## 🚀 Installation

### 🔹 HACS (empfohlen)

1. Öffne **HACS**
2. Suche nach **powerHELPER**
3. auf **Herunterladen** klicken
4. Home Assistant neu starten

---

### 🔹 Manuelle Installation

1. Repository herunterladen
2. Ordner `power_helper` kopieren nach: `config/custom_components/`
3. Home Assistant neu starten

---

## ⚙️ Konfiguration

1. **Einstellungen → Geräte & Dienste**
2. **Integration hinzufügen**
3. **powerHELPER** auswählen
4. Gerätenamen festlegen
5. Leistungssensoren auswählen

---

## 🧠 Erzeugte Sensoren

### 🔌 Netz

#### Input
- `sensor.gerät_netz_leistung` — Netz Leistung
- `sensor.gerät_netzbezug` — Netzbezug
- `sensor.gerät_netzeinspeisung` — Netzeinspeisung
#### Leistungsfluss
- `sensor.gerät_netz_zu_haus` — Netz → Haus
- `sensor.gerät_netz_zu_akku` — Netz → Akku

### ☀️ PV
#### Input
- `sensor.gerät_pv_leistung` — PV Leistung
#### Leistungsfluss
- `sensor.gerät_pv_zu_haus` — PV → Haus
- `sensor.gerät_pv_zu_akku` — PV → Akku
- `sensor.gerät_pv_zu_netz` — PV → Netz

### 🔋 Akku
#### Input
- `sensor.gerät_akku_leistung` — Akku Leistung
- `sensor.gerät_akku_leistung_invertiert` — Akku Leistung invertiert
- `sensor.gerät_akku_laden` — Akku laden
- `sensor.gerät_akku_entladen` — Akku entladen
#### Leistungsfluss
- `sensor.gerät_akku_zu_haus` — Akku → Haus
- `sensor.gerät_akku_zu_netz` — Akku → Netz

### 🏠 Haus
- `sensor.gerät_haus_leistung` — Haus Leistung

Alle Sensoren liefern **Watt (W)** und sind Dashboard-fähig.

---

## ❓ FAQ

### Benötige ich AC oder DC Sensoren?

Im Allgemeinen sollten alle Sensoren für diese Bilanz AC-Leistungen sein, da diese die tatsächlichen Leistungsflüsse im Stromkreis darstellen.

DC-Sensoren, wie sie beispielsweise von Wechselrichtern direkt aus der PV-Anlage oder bestimmten Akkuspeichern kommen, können ebenfalls genutzt werden. In diesem Fall spiegeln sich die DC/AC-Wandlungsverluste einfach in der **Haus Leistung** wider, wodurch der Gesamtverbrauch des Hauses entsprechend steigt, ähnlich wie bei anderen elektrischen Verbrauchern.

---

## 🧪 Status

Version: **1.0.7**

Getestet mit PV + Akku Systemen

---

## 📄 Lizenz

MIT License

Copyright (c) 2026 Dennis

---