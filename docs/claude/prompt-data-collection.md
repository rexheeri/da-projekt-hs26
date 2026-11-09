# Auftrag für Claude Code: Datenerhebung und Daten-Issues (DA Gruppe 3)

Erstellt am 03.11.2026 für Erion (ER). Ablage im Repo: `docs/claude/prompt-data-collection.md`.
Start in Claude Code: «Lies `docs/claude/prompt-data-collection.md` und beginne mit Phase 0.»
Fortsetzen nach einem Unterbruch: «Lies den Prompt und `docs/project-state.md` und mach bei Phase X weiter.»

---

## 1. Ziel

Erhebe **alle Daten** für unsere Forschungsfrage per Skript, lade sie in die
Datenbank, verknüpfe die Quellen in SQL und arbeite danach die **Daten- und
Datenbank-Issues** ab, bis sie nachweisbar erfüllt sind.

Forschungsfrage (siehe `docs/research-design.md`): Steigt bei Regen oder Schnee
die Wahrscheinlichkeit einer Ankunftsverspätung ≥ 3 Min. im Regionalverkehr
stärker als im Fernverkehr? Grossraum Zürich, einige Wintermonate.

Was wir dem Dozenten zugesagt haben (Mail an Gellrich, Antwort 28.10.2026):
- Quelle 1: **Ist-Daten** von opentransportdata.swiss (Soll- und Ist-Zeiten pro Halt und Tag),
  **per Skript über die API** heruntergeladen. Das zählt laut Gellrich als eigene Datenerhebung.
- Quelle 2: **MeteoSchweiz-Messwerte** über die **STAC-API**.
- Verknüpfung über **Zeitstempel und nächstgelegene Wetterstation** zu jeder Haltestelle.
- Datenbank: **PostgreSQL** (ersetzt SQLite, gibt Zusatzpunkt). SQLite bleibt Fallback, gleicher Code über `src/db.py`.

## 2. Lies zuerst

1. `CLAUDE.md` (Regeln, bindet `docs/project-state.md` und `docs/grading.md` ein)
2. `docs/research-design.md` (Variablen, DECIDE- und VERIFY-Punkte, Hypothesen)
3. `.claude/agents/data-pipeline.md` (Pipeline-Regeln). Für Pipeline-Code diesen Agenten verwenden.
4. `docs/integration-log.md`, `docs/ai-log.md`
5. `gh issue list --state all --limit 50` und ordne die Issue-**Titel** ihren Nummern zu.
   Nummern in diesem Prompt nie annehmen, immer über den Titel gehen.

## 3. Arbeitsweise (verbindlich)

- **Phasen mit CHECKPOINT.** An jedem CHECKPOINT hörst du auf, berichtest kurz
  (Tabelle statt Fliesstext) und wartest auf Erions OK. Nie über einen
  CHECKPOINT hinweg weiterarbeiten.
- **Klein anfangen:** ein Tag → eine Woche → ganzer Zeitraum. Grosse Downloads
  erst, wenn ein Tag end-to-end funktioniert und Erion die Grössenschätzung
  freigegeben hat.
- **VERIFY statt annehmen.** Spaltennamen, Werte, Parametercodes, Zeitzonen und
  URL-Muster stellst du aus der echten Quelle fest und zeigst sie. Was du nicht
  belegen kannst, nennst du offen. Nichts aus dem Gedächtnis als Fakt ausgeben.
- **DECIDE-Punkte entscheidest du nicht.** Du machst einen Vorschlag mit Zahlen
  aus den Daten, Erion entscheidet. Eintrag dann als «decided by ER on <Datum>,
  team to confirm».
- **Git:** vor dem Start `git pull`. Pro Issue ein Branch `<nr>-<kurz>`, kleine
  Commits auf Englisch, PR mit «Closes #<nr>». Gemergt wird erst nach Erions OK
  (er darf das an einem CHECKPOINT für mehrere PRs gesammelt geben). Kein
  Force-Push, kein `reset --hard`, keine gelöschten Branches.
- **Nie committen:** Rohdaten, `data/processed/`, Datenbankdateien, Parquet,
  ZIP, `.env`. Vor jedem Commit `git status` prüfen.
- **Code-Regeln aus `CLAUDE.md` §5 gelten ohne Ausnahme.** Code ist kommentiert
  (Docstring pro Datei und Funktion, Kommentar bei jedem nicht offensichtlichen
  Schritt), Pfade über `src/paths.py`, DB über `src/db.py`, portables SQL,
  Joins und Aggregationen in SQL. Einfache Funktionen, keine Klassenhierarchien:
  Alle drei müssen den Code im Video erklären können.
- **Logs sofort:** nach jedem Download, jeder Bereinigung und jedem Join ein
  Eintrag in `docs/integration-log.md` (Zeilen vorher/nachher, verloren,
  Grund), nach jeder Aufgabe eine Zeile in `docs/ai-log.md` (Tool «Claude Code»,
  was falsch war oder korrigiert werden musste, ehrlich).
- **Stand sichern:** An jedem CHECKPOINT `docs/project-state.md` nachführen
  (Datentabelle, Entscheide, Change log), committen und pushen. So kann eine
  neue Sitzung nach einem Unterbruch nahtlos weitermachen.
- **Zeitrahmen:** ER is not available from 07.11. to 15.11. **Phase 1 und 2
  müssen bis Fr 06.11. abgeschlossen und gepusht sein**, damit Lorenzo und
  Levin vor der Konzeptpräsentation am 17.11. damit weiterarbeiten können.
- Terminal ist Windows (PowerShell). Lange Läufe mit Fortschrittsanzeige und
  so, dass ein Abbruch keinen Schaden anrichtet (wiederaufnehmbar).

## 4. Phasen

### Phase 0 — Vorbereitung (kurz)

- `git pull`, `python -m src.check_setup`, `gh auth status`
- Freier Speicherplatz auf dem Laufwerk des Repos (Python `shutil.disk_usage`)
- Läuft Docker? (`docker info`) Wenn ja: `docker compose up -d`, `DATABASE_URL`
  in `.env` setzen (Erion trägt das Passwort selbst ein, du liest `.env` nicht)
  und ab Phase 2 direkt auf PostgreSQL arbeiten. Wenn nein: SQLite, Umstieg in Phase 4.
- Zuordnung Issue-Titel → Nummer als Tabelle

**CHECKPOINT 0:** Setup-Status, Speicherplatz, DB-Backend, Issue-Tabelle.

### Phase 1 — Quellen erkunden und Machbarkeit prüfen

Issues: «Ist-Daten: API download prototype for one day», «Weather: STAC API
prototype for one day (Zurich stations)», «Weather: find rain/snow days in
Zurich and choose the study period», «Stops: coordinates and nearest weather station».

**1a Haltestellen** (zuerst, weil der Zürich-Filter davon abhängt)
- Dienststellen-/Haltestellenverzeichnis per Skript holen (opentransportdata.swiss
  bzw. atlas). Gesucht: Haltestellennummer, die zur Ist-Daten-Spalte `BPUIC`
  passt, Koordinaten, Kanton.
- Studiengebiet festlegen: Vorschlag Kanton ZH. Wie viele Bahnhaltestellen?

**1b Ist-Daten**
- Herausfinden und belegen, wie man **per Skript** an die Tagesdateien kommt:
  - aktueller Monat: CKAN-API von `data.opentransportdata.swiss` (Datensatz `istdaten`)
  - frühere Monate: Archiv `https://archive.opentransportdata.swiss/` (laut Betreiber
    Monats-ZIPs mit Tagesdateien, ab 2016 bis zum letzten vollen Monat).
    Dokumentierter Einstiegspunkt: Übersichtsseite
    `https://archive.opentransportdata.swiss/actual_data_archive.htm`
    (Liste aus `istdaten.php`). Dort liegen auch Fahrplan-Archive (GTFS,
    HRDF, NeTEx): nur prüfen, nichts ohne OK herunterladen.
  - Nachtrag 03.11.2026: Die CKAN-Action-API antwortet 403. Die Dateiliste
    des Portals kommt aus dem DCAT-Katalog (JSON-LD).
  - URL-Muster per Skript ermitteln, Dateigrössen per HEAD-Request feststellen,
    nichts Grosses herunterladen.
- **Einen Tag** herunterladen (über die CKAN-API), einlesen, zeigen: echte
  Spalten, Datentypen, Trennzeichen, Zeilenzahl roh, 5 Beispielzeilen.
- **VERIFY** (Ergebnis in `research-design.md` eintragen): Werte von
  `AN_PROGNOSE_STATUS` und ihr Anteil, Ausfallflag (`FAELLT_AUS_TF`),
  Zusatzfahrten, welche Spalte die Zugkategorie trägt (S, RE, IR, IC …),
  Format und **Zeitzone** der Zeitstempel.
- Früh filtern: nur Zug, nur Haltestellen im Studiengebiet, nur benötigte
  Spalten. Zeilenzahl nach Filter.

**1c Wetter**
- STAC-Collection `ch.meteoschweiz.ogd-smn` (Endpoint
  `https://data.geo.admin.ch/api/stac/v1`, Doku opendatadocs.meteoswiss.ch) mit
  `pystac-client`. Stationsmetadaten (Koordinaten, **Höhe**) und
  `ogd-smn_meta_parameters.csv` laden.
- Offizieller Weg für den automatischen Download:
  `https://opendatadocs.meteoswiss.ch/general/download#how-to-download-files-automatically`
  (STAC-API, `If-None-Match`/ETag, Retries mit truncated exponential backoff
  und Jitter). Historical (bis 31.12. Vorjahr) und recent (ab 01.01.) ohne
  Lücke und ohne Doppel zusammenführen.
- Referenz, keine Datenquelle: `https://github.com/MeteoSwiss` (opendata,
  weathermart, PeakWeather). Fertige Datensätze höchstens als Gegencheck.
- Weitere Sammlungen prüfen: `https://opendatadocs.meteoswiss.ch/` (A–D) und
  `https://opendatadocs.meteoswiss.ch/c-climate-data`. Niederschlagsnetz
  `ch.meteoschweiz.ogd-smn-precip` wird genutzt (Entscheid 03.11.2026).
- **Parametercodes aus der Metadatei belegen, nicht raten:** stündliche
  Niederschlagssumme, Lufttemperatur 2 m, Schneehöhe.
- Stationen im und um das Studiengebiet auflisten (Kürzel, Name, Höhe,
  Distanz). **Gipfelstationen** (deutlich höher als die Bahnlinien) als
  Vorschlag ausschliessen, mit Begründung.
- **VERIFY:** Zeitzone der Zeitstempel (vermutlich UTC, Ist-Daten vermutlich
  Lokalzeit) und welches Intervall ein Stundenwert abdeckt (Beginn oder Ende
  der Stunde). Ein Fehler hier verschiebt jeden Join um eine bis zwei Stunden.
  Ergebnis mit einem konkreten Beispiel belegen.

**1d Studienzeitraum und Machbarkeit**
- Mit Tageswerten für die Winter 2023/24, 2024/25, 2025/26: Tage trocken /
  Regen / Schnee pro Monat je Station. Zwei Schnee-Definitionen nebeneinander
  zeigen: (1) Niederschlag bei Temperatur ≤ 0 °C (Vorschlag aus research-design),
  (2) Zunahme der Schneehöhe.
- Vorschlag Studienzeitraum (Monate) mit Begründung.
- Schätzung für diesen Zeitraum: Download-Volumen, Speicherbedarf (roh und
  gefiltert), Laufzeit.
- Stationszuordnung: nächste Station je Haltestelle (geopandas, projiziert in
  LV95 / EPSG:2056), Distanz in km, Median und Maximum, Haltestellen > 10 km markieren.

**CHECKPOINT 1 (der wichtigste):** eine Übersicht mit
- verifizierten Spalten und VERIFY-Ergebnissen,
- Zugangsweg je Quelle (CKAN-API / Archiv / STAC), inkl. Hinweis, ob die
  Winterdaten nur über das Archiv erreichbar sind,
- Stationsliste mit Ausschlussvorschlag,
- Tabelle Schnee-/Regentage pro Monat, Vorschlag Studienzeitraum,
- Grössen- und Laufzeitschätzung,
- Vorschlägen mit Zahlen für alle DECIDE-Punkte (Schwelle 3 Min. mit Quelle,
  Zuordnung Verkehrsart inkl. IR, Niederschlagskategorien, Ausfälle, nur
  gemessene Zeiten, Effektmass, Studienzeitraum).

Warte auf Erions Entscheide. Trag sie danach in `research-design.md` und
`project-state.md` ein.

### Phase 2 — Prototyp end-to-end (ein Tag, dann eine Woche)

Issues: «Database schema and loading of prototype data», «Join arrivals → stop
→ nearest station → hour», «Stops: …» (Abschluss), «First EDA for the presentation».

- Schema-Vorschlag: `stops`, `weather_stations`, `stop_station`,
  `weather_hourly`, `arrivals`. Laden über `src/db.write_table`.
- Join **in SQL**: arrivals × stop_station × weather_hourly über Haltestelle,
  Station und Stunde. Die Stunde rechnest du vorher in pandas (in einer
  einheitlichen Zeitzone) und speicherst sie als Spalte.
- Tabelle oder View `analysis_base` mit allen Variablen aus research-design
  (`delayed`, `traffic_type`, `precip_cat`, `precip_mm`, `temp_c`, `hour`,
  `weekday`, `rush_hour`, `holiday`) plus zwei Variablen gegen den
  Fernverkehr-Bias (research-design §4, «Plausible counter-result»):
  - `entry_delay`: Verspätung der Fahrt beim ersten Halt im Studiengebiet
  - `delay_gain`: Verspätungszunahme gegenüber dem vorherigen Halt derselben Fahrt
  Beide nur aus Informationen, die vor der Ankunft bekannt sind (kein Leakage).
- Stichprobe: 5 Zeilen von Hand gegen die Rohdaten prüfen und das Ergebnis zeigen.
- Integration-Log: jeder Schritt mit Zeilen vorher/nachher und Verlustgrund.
- Danach dasselbe für eine Woche. Prüfen, ob Laufzeit und Speicher zur
  Schätzung aus Phase 1 passen.
- **Erste EDA:** Notebook über `/new-notebook` (Initialen `er`), Daten per SQL
  aus der DB. Inhalt laut Issue: Datenstruktur (Zeilen, Spalten, Typen,
  fehlende Werte), Verspätungsquote je Verkehrsart × trocken/Regen/Schnee
  (Tabelle per `GROUP BY` und Balkendiagramm), Verteilung der Verspätungen.
  Grafiken in Folienqualität (Titel = Aussage, Achsen, n, Quelle), deutlich
  als «preliminary» markiert, als PNG nach `presentation/figures/`.
  `list_tables()` und ein einfaches ER-Diagramm für die Folie «data structure».

**CHECKPOINT 2:** `list_tables()`, Verluste im Join, erste Tabelle der
Verspätungsquoten, Grafiken, offene PRs. Bis Fr 06.11. gemergt und gepusht.

### Phase 3 — Volle Pipeline für den Studienzeitraum

Issue: «Full pipeline for the whole study period».

- Erst nach Erions OK zur Grössenschätzung starten.
- Idempotent und wiederaufnehmbar: bereits verarbeitete Tage überspringen.
- Tage direkt aus dem ZIP lesen (`zipfile`, nicht entpacken), sofort filtern,
  pro Tag ein kleines Parquet in `data/processed/`. Ob die Roh-ZIPs danach
  bleiben oder gelöscht werden, entscheidet Erion (Speicher).
- Qualitätsbericht: fehlende Tage, Duplikate, Anteil gemessener Zeiten,
  Ausfälle, Haltestellen ohne Station, Stunden ohne Wetterwert.
- Ein Einstiegspunkt für den Neuaufbau, z. B. `python -m src.pipeline`, mit
  Anleitung im README. Test: frischer Clone, ein Tag, läuft durch.
- **Datenweitergabe ans Team:** Die Daten liegen nicht im Git und eine
  PostgreSQL-Instanz auf Erions Laptop ist für die anderen nicht erreichbar.
  Baue deshalb einen kompakten Export (`analysis_base`, `stops`,
  `weather_stations`, `stop_station`, `weather_hourly` als Parquet) und
  ein Ladeskript (z. B. `python -m src.load_shared <ordner>`), mit dem
  Lorenzo und Levin die Daten in ihre eigene DB laden. Erion legt den Export in
  OneDrive/Teams ab. Grösse angeben.

**CHECKPOINT 3:** Zeilen je Tabelle, Qualitätsbericht, Laufzeit, Exportgrösse, PRs.

### Phase 4 — PostgreSQL und Export für die Abgabe

Issues: «Switch to PostgreSQL (bonus)», «Data export for the submission zip (all data must be included)».

- Falls noch auf SQLite: auf PostgreSQL umstellen, volle Pipeline dort laufen
  lassen, `check_setup` zeigt postgresql. Screenshot-Anleitung (pgAdmin oder
  Query-Ausgabe) für den Selbsteinschätzungs-Anhang notieren.
- Export für die Abgabe-ZIP als Skript nach `data/export/` (baut auf dem
  Team-Export aus Phase 3 auf, plus Rohdaten-Stichprobe je Quelle). Grösse prüfen.
  Den Punkt «notebooks run on the exported data only» kannst du erst prüfen,
  wenn die Analyse-Notebooks existieren. Issue deshalb **offen lassen** und
  den Stand kommentieren.

**CHECKPOINT 4:** Stand beider Issues.

### Phase 5 — Abschluss

- `docs/project-state.md`: Datentabelle (Status «done» je Quelle, Zeitraum,
  Zeilen), Entscheide, Change log.
- `docs/ai-log.md`: ehrliche Einträge inkl. Fehler, die korrigiert werden mussten.
- Kurze **Übergabe für Lorenzo und Levin** als Abschnitt in
  `docs/onboarding.md`: wo die Daten liegen, wie man sie lädt, was in
  `analysis_base` steht (Spalten mit Bedeutung), welche Issues jetzt
  freigeschaltet sind.
- Schlussbericht an Erion: Tabelle Issue → Status (geschlossen / offen und warum) → PR.

## 5. Regeln für Issues

- **Schliessen nur, wenn jede Checkbox im Issue-Text erfüllt ist.** Checkboxen
  per `gh issue edit` abhaken, dazu ein Kommentar mit dem Nachweis (Zahlen,
  Dateien, PR-Link). Geschlossen wird über den PR («Closes #nr») beim Merge.
- Teilweise erfüllt: offen lassen, kommentieren, was fehlt und wer es braucht.
- «Weather: find rain/snow days … choose the study period» und «Decide variable
  definitions» erst schliessen, wenn Erion die Entscheide getroffen hat.
- **Nicht bearbeiten und nicht schliessen** (Personen-, Team- oder
  Analyseaufgaben der Rollen B/C):
  Onboarding Lorenzo · Onboarding Levin · Assign roles · Reply to lecturer
  (höchstens einen Antwortentwurf im Chat liefern) · Concept presentation
  slides · Dry run · After the presentation · Complete EDA · Map · Hypothesis
  tests · Classification · k-means · Stats review · Final presentation PDF ·
  Video · AI reflection summary · Submission package.
  Grund: Jede Person muss im Video ihren eigenen Teil frei erklären können, und
  diese Issues gehören zu den Rollen, die das Team im Call verteilt.
- Neue Probleme, die du findest, als neues Issue mit Label und Milestone
  vorschlagen. Anlegen erst nach OK.

## 6. Was du nicht tust

- Keine Modelle, Tests oder Interpretationen der Ergebnisse. Die erste EDA
  bleibt beschreibend.
- Keine Termine, Fristen oder Punkte erfinden. `docs/grading.md` nicht ändern.
- `.env` nicht lesen. Keine API-Keys im Code.
- Keine manuellen Downloads vorschlagen. Alles, was in die Analyse eingeht,
  kommt über ein Skript in `src/`.
- Die Nutzungsbedingungen der Quellen einhalten: kurze Pausen zwischen
  Requests, keine parallelen Massendownloads.
