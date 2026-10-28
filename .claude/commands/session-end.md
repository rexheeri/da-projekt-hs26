---
description: Sitzung abschliessen — Logs und Projektstand nachführen, Commit vorschlagen
---

Schliesse die Sitzung sauber ab.

1. **KI-Log:** Gab es in dieser Sitzung nennenswerte KI-Hilfe? Dann einen
   Eintrag für `docs/ai-log.md` vorschlagen (Format wie `/ai-log`).
2. **Integration-Log:** Gab es neue Quellen, Joins oder Bereinigungen? Dann
   eintragen (Format wie `/integration-log`).
3. **`docs/project-state.md`:** Nachführen, was sich geändert hat: Datenstatus,
   Haken im Zeitplan, neue Entscheide mit Grund, Antworten des Dozenten, eine
   Zeile im Change log. «Last updated» mit Datum und Initialen setzen. Nur
   ändern, was sich wirklich geändert hat. Die Datei soll kurz bleiben.
4. **Git:** `git status` zeigen. Prüfen, dass keine Daten, `.sqlite`, `.env`
   oder grossen Dateien dabei sind. Eine englische Commit-Message vorschlagen.
   Committen und pushen erst nach ausdrücklichem OK.
5. Zum Schluss den **nächsten Schritt** in einem Satz nennen.

Zeig alle Änderungen an den `docs/`-Dateien vor dem Speichern.
