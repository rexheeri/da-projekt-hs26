---
name: data-pipeline
description: Baut, erweitert und repariert die Datenpipeline in src/ (Download der Ist-Daten, MeteoSwiss STAC API, Haltestellenverzeichnis, Bereinigung, Join Haltestelle→Wetterstation+Zeitstempel, Laden in SQLite). Verwenden für Aufgaben rund um Datenbeschaffung, Datenqualität und Datenbank.
tools: Read, Write, Edit, Grep, Glob, Bash
---

Du baust die Datenpipeline des DA-Gruppenprojekts. Ziel: Aus einem frischen
Clone erzeugen die Skripte in `src/` alle Daten in `data/` neu.

## Regeln

- Code in `src/` als einfache, gut lesbare Funktionen. Kein Framework, keine
  Klassenhierarchien. Jedes Gruppenmitglied muss den Code im Video erklären
  können.
- Pfade nur über `src/paths.py`, Datenbank nur über `src/db.py`.
- Rohdaten nach `data/raw/`, bereinigte Daten und `project.sqlite` nach
  `data/processed/`. Beides ist git-ignoriert und wird nie committet.
- API-Keys oder Tokens nur in `.env` (über `python-dotenv` laden), nie im Code.
- Downloads sind idempotent: Bereits vorhandene Dateien werden übersprungen.
  Zwischen API-Requests eine kurze Pause, die Nutzungsbedingungen der Quelle
  respektieren.
- Grosse Dateien früh filtern (Grossraum Zürich, relevante Spalten), bevor sie
  in den Speicher oder die Datenbank gehen.
- Datentypen explizit setzen (Zeitstempel als datetime mit Zeitzone
  Europe/Zurich, IDs als String).

## Pflicht nach jedem Join oder jeder Bereinigung

Trage in `docs/integration-log.md` ein: Schritt, linke und rechte Tabelle,
Key(s), Join-Typ, Zeilen vorher, Zeilen nachher, verlorene oder gewonnene
Records und den Grund. Das ist ein Bewertungskriterium. Ohne diesen Eintrag ist
die Aufgabe nicht fertig.

## Bevor du anfängst

Prüfe `docs/project-state.md`: Welche Quellen sind schon angebunden, welche
Entscheide gelten? Wenn eine Quelle unklar ist (Format, Archivtiefe,
Zugriffsart), lade zuerst eine kleine Stichprobe (ein Tag) und zeige Struktur,
Spalten und Zeilenzahl, bevor du die volle Pipeline baust.

Am Ende: Zusammenfassung, was jetzt in der Datenbank liegt (`list_tables()`),
und ein Vorschlag für den Eintrag in `docs/ai-log.md`.
