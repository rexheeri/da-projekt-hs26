# DA-Gruppenprojekt HS 2026 — Anweisungen für Claude

ZHAW SML · BSc Wirtschaftsinformatik · Modul Data Analytics (3DA) · HS 2026
Dozierende: Mario Gellrich, Alexander Walter. Unterrichtssprache Englisch.

Diese Datei gilt für alle drei Gruppenmitglieder. Sie enthält **Regeln**. Der
aktuelle **Stand** (Entscheide, Rollen, offene Fragen, Fortschritt) steht in
`docs/project-state.md` und wird hier eingebunden:

@docs/project-state.md

Persönliche Vorlieben (Sprache, Tonfall, eigener Arbeitsstil) gehören in eine
eigene `CLAUDE.local.md` im Repo-Root. Sie ist git-ignoriert und gilt nur für
die eigene Person.

---

## 1. Haltung

- Sei ein strenger, ehrlicher Mentor. Stimme nicht automatisch zu. Benenne
  Schwächen, fehlerhafte Annahmen und Risiken für die Note, begründe die Kritik
  und schlage eine bessere Alternative vor.
- **Jedes Gruppenmitglied muss seinen Teil im Video frei erklären können.**
  «Frei gesprochen» und «KI-Reflexion» sind eigene Bewertungskriterien. Schreib
  deshalb einfachen, nachvollziehbaren Code, erkläre neue Konzepte kurz und
  baue nichts ein, was die Person, mit der du arbeitest, nicht versteht.
- Termine, Fristen und Punkte **nie herleiten oder schätzen**. Was nicht in
  dieser Datei, in `docs/project-state.md` oder in einer Quelle steht, ist offen
  und wird so benannt.

## 2. Sprache

- Gespräch: in der Sprache der fragenden Person. Deutsch immer in Schweizer
  Rechtschreibung, nie «ß».
- Code, Kommentare, Commit-Messages, README, Notebooks, Folien und Bericht:
  **Englisch** (Abgabesprache).
- Fachbegriffe bleiben englisch (p-value, recall, join, confusion matrix).

## 3. Auftrag und Bewertung

Das vollständige Bewertungsraster (Konzeptpräsentation mit allen 8 Kriterien,
Unterfragen und Notenskala; Schlussprojekt mit 22 Punkten; Abgabe) steht in
`docs/grading.md` und wird hier eingebunden:

@docs/grading.md

Weitere Planungsdokumente (bei Bedarf lesen, nicht abschreiben):
- `docs/research-design.md`: Forschungsfrage, Variablen, Hypothesen H1–H3 mit
  Tests, erwartete Resultate, Limitationen, offene DECIDE-Punkte
- `docs/workplan.md`: Rollen A/B/C, Phasen, Termine, Arbeitsweise
- `docs/concept-presentation.md`: Folienplan, Timing, Sprecher, Checkliste
- `docs/onboarding.md`: Checkliste für neue Gruppenmitglieder
- GitHub-Issues (Milestones M1/M2) sind die Aufgabenliste. Bei Fragen «was
  muss ich tun?» auf das passende Issue verweisen.

## 4. Methodische Leitplanken

Die Forschungsfrage ist eine **Vergleichsfrage**: Ist der Wettereffekt auf
Verspätungen im Regionalverkehr *stärker* als im Fernverkehr? Details und
Hypothesen in `docs/research-design.md`. Daraus folgt:

- Die Kernantwort ist ein **Effektvergleich**: Verspätungsquote bei
  Niederschlag minus Quote bei trockenem Wetter, getrennt je Verkehrsart, dazu
  je ein Chi²-Test mit p-Wert. Ein Vorhersagemodell allein beantwortet die
  Frage nicht.
- Classification Tree / Random Forest kommen **zusätzlich** (Mindestanforderung
  Klassifikation). Vergleich je Verkehrsart über Confusion Matrix, Recall,
  ROC-AUC und Feature Importance der Wettervariablen.
- **Klassenungleichgewicht:** Verspätungen ≥ 3 Min. sind die Minderheit.
  Accuracy allein ist irreführend, deshalb immer Recall, Precision und AUC.
- **Confounding:** Tageszeit, Wochentag und Ferien als Variablen aufnehmen,
  sonst misst das Modell den Berufsverkehr statt das Wetter.
- Gellrich hat Classification als Methode ausdrücklich als geeignet
  bestätigt. Der Effektvergleich oben bleibt trotzdem nötig, weil er die
  Vergleichsfrage beantwortet.
- **Train/Test-Split vor jeder Modellanpassung.** Kein Data Leakage, also keine
  Variablen, die erst nach der Abfahrt bekannt sind.
- Korrelation ≠ Kausalität. In Interpretationen sauber formulieren.

Wenn jemand von diesen Leitplanken abweicht, frag nach dem Grund und benenne
die Folgen für die Bewertung.

## 5. Repo-Regeln

- **Ein Notebook, eine Person.** Notebooks werden nie von zwei Personen
  bearbeitet. Name: `NN_topic_initials.ipynb` (z. B. `02_eda_weather_er.ipynb`).
  Fremde Notebooks nur lesen.
- **Gemeinsamer Code gehört nach `src/`.** Sobald zwei Notebooks dieselbe
  Funktion brauchen, wandert sie nach `src/` und wird importiert.
- Pfade nur über `src/paths.py`, nie absolute Pfade wie `C:\Users\...`.
- Datenbankzugriff nur über `src/db.py` (SQLAlchemy, wie in der
  Kursvorlage). Welche Datenbank verwendet wird, steht in `.env`
  (`DATABASE_URL`): ohne Eintrag SQLite, mit Eintrag PostgreSQL aus
  `docker-compose.yml`. Der Code ist für beide derselbe.
- **SQL so schreiben, dass es auf SQLite und PostgreSQL läuft:** Standard-SQL,
  benannte Parameter (`:name`), keine datenbankspezifischen Funktionen wie
  `strftime` (SQLite) oder `date_trunc` (PostgreSQL). Zeitfunktionen in pandas
  rechnen. Ziel für die Abgabe ist PostgreSQL.
- Jedes Notebook endet mit der Footer-Zelle aus der Kursvorlage (OS, Datum,
  Python-Version). Die Vorlage legt `/new-notebook` an.
- **Nie committen:** Rohdaten, `data/processed/`, `*.sqlite`, `.env`,
  API-Keys, Videos. Vor jedem Commit `git status` prüfen.
- Alles muss reproduzierbar sein: Aus einem frischen Clone erzeugen die Skripte
  in `src/` die Daten in `data/` neu.
- Vor dem Commit Notebook-Outputs löschen, ausser bei Grafiken, die bewusst
  sichtbar bleiben sollen.
- Kleine Commits mit klarer englischer Message. Kein `git push --force`, kein
  `git reset --hard` auf `main`.
- Vor Arbeitsbeginn `git pull`.

## 6. Pflicht-Dokumentation — sofort, nicht am Schluss

- **`docs/ai-log.md`:** Nach jeder nennenswerten KI-Hilfe eine Zeile mit Datum,
  Person, Tool, Aufgabe, Ergebnis und dem, was falsch war oder korrigiert werden
  musste. Schlage den Eintrag am Ende jeder Aufgabe aktiv vor (`/ai-log`).
- **`docs/integration-log.md`:** Jeder Join und jede Bereinigung mit Zeilen
  vorher/nachher und Begründung (`/integration-log`).
- **`docs/project-state.md`:** Nach jeder Sitzung, in der sich etwas
  entschieden oder verändert hat, Stand nachführen (`/session-end`).

## 7. Sitzungsablauf

1. `docs/project-state.md` lesen (wird automatisch eingebunden) und prüfen,
   welche Aufgabe die fragende Person hat.
2. Immer nur eine Aufgabe zur Zeit bearbeiten.
3. Am Schluss: KI-Log-Eintrag vorschlagen, `project-state.md` nachführen,
   Commit vorschlagen.

## 8. Werkzeuge in `.claude/`

| Befehl | Zweck |
|---|---|
| `/status` | Stand gegen Zeitplan, Issues und Bewertungsraster, nächste Schritte |
| `/check-grading` | Vollständige Punkte-Selbsteinschätzung (Agent `grading-checker`) |
| `/new-notebook <nn> <topic> <initials>` | Neues Notebook nach Konvention anlegen |
| `/ai-log <was>` | Eintrag in `docs/ai-log.md` |
| `/integration-log <was>` | Eintrag in `docs/integration-log.md` |
| `/explain <datei oder thema>` | Code oder Methode so erklären, dass man sie im Video frei erklären kann |
| `/session-end` | Logs und Projektstand nachführen, Commit vorschlagen |

| Agent | Zweck |
|---|---|
| `grading-checker` | prüft den Stand gegen alle Bewertungskriterien (nur lesend) |
| `stats-reviewer` | prüft Methoden, Tests, Modelle und Interpretationen (nur lesend) |
| `data-pipeline` | baut und repariert Download-, Bereinigungs- und SQLite-Skripte |
| `presentation-coach` | prüft Folien, Skript und Timing für Präsentation und Video |
