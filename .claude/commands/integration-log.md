---
description: Eintrag in docs/integration-log.md (Join, Bereinigung, Inkonsistenz)
argument-hint: <welcher Schritt>
---

Dokumentiere einen Integrationsschritt in `docs/integration-log.md`. Kontext:
$ARGUMENTS

- Neue Quelle → Tabelle «Sources» (Datei/Endpoint, Zeitraum, Zeilen roh,
  Abrufdatum, Person)
- Join → Tabelle «Joins» (linke/rechte Tabelle, Keys, Join-Typ, Zeilen vorher,
  Zeilen nachher, verloren/gewonnen, Grund)
- Problem in den Daten → Tabelle «Inconsistencies found»

Die Zeilenzahlen nicht schätzen. Ermittle sie mit Code (`src/db.py` oder dem
betroffenen Notebook) oder frag nach. Englisch, knapp. Zeig den Eintrag vor dem
Speichern.
