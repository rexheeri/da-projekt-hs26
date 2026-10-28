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
- **Jeder Code ist kommentiert:** Docstring pro Datei und Funktion,
  Kommentar bei jedem nicht offensichtlichen Schritt (was und warum).
- Pfade nur über `src/paths.py`, Datenbank nur über `src/db.py`.
- Rohdaten nach `data/raw/`, bereinigte Zwischenstände nach
  `data/processed/`. Beides ist git-ignoriert und wird nie committet.
- Die Datenbank ist SQLite oder PostgreSQL, je nach `DATABASE_URL` in `.env`.
  SQL muss auf beiden laufen: Standard-SQL, benannte Parameter `:name`,
  Datums- und Zeitlogik in pandas statt in SQL.
- Downloads laufen **per Skript über die API**. Das hat der Dozent als eigene
  Datenerhebung akzeptiert. Manuell heruntergeladene Dateien zählen nicht.
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
