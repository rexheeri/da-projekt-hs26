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

## 3. Auftrag und Bewertung (Quelle: Moodle-Kursseite, Stand 06.10.2026)

| Teil | Gewicht | Termin |
|---|---|---|
| Schriftliche Prüfung (einzeln, open book) | 60 % | offen |
| Konzeptpräsentation (Gruppe, 10 Min., vor Ort, Präsenzpflicht) | 20 % | Di 17.11.2026, 11:00–12:45, SW301 |
| Schlussprojekt (Gruppe) | 20 % | 10.01.2027, 23:59 |

### Konzeptpräsentation — 8 Kriterien, je Note 1–6, Durchschnitt
1. Struktur
2. Background & Problemstellung
3. Ziel & Forschungsfrage
4. Daten (Quelle **und Struktur erklärt**)
5. Methoden (passend und begründet)
6. Erwartete Resultate
7. Frei gesprochen
8. Folienqualität

Inhalt ist das Konzept, nicht das fertige Projekt. Aber Kriterium 4 lässt sich
nur gut erfüllen, wenn bis dahin **echte Daten** geladen sind.

### Schlussprojekt — max. 22 Punkte
**Mindestanforderungen (9 P)**
- Eigene Datenerhebung per Web Scraping oder Web API (kein Kaggle als Hauptquelle)
- ≥ 2 Quellen integriert; Integration dokumentiert: Keys, Joins,
  Inkonsistenzen, Records verloren/gewonnen → `docs/integration-log.md`
- SQLite-Datenbank, Abfragen mit SQL aus Python → `src/db.py`
- EDA tabellarisch **und** grafisch
- Regression oder Klassifikation mit einer Forschungsfrage, die über eine
  Standardprognose hinausgeht (Vergleich von Gruppen, Regionen, Zeiträumen
  oder Quellen)
- Measures of fit und korrekte Interpretation
- KI-Nutzung dokumentiert (Vor- und Nachteile, wo es scheiterte) → `docs/ai-log.md`
- Material auf Moodle

**Zusatzpunkte (max. 6 P):** Kreativität · PostgreSQL o. ä. statt SQLite ·
Geodaten · Chi², ANOVA oder Korrelation mit p-Wert · zusätzlich k-means ·
öffentliches GitHub-Repo (URL in den Folien)

**Video (max. 7 P):** Länge = Anzahl Personen × 5 Min. (3 Personen → 15 Min.).
Bewertet: Struktur, Thema, Inhalt, frei gesprochen, Folien, KI-Reflexion,
Zeiteinhaltung. **Nicht durch Notebooks scrollen.**

**Abgabe (eine Person für die Gruppe):**
- `video_recording_group_XX.mp4` (ggf. in Teilen)
- `materials_group_XX.zip` (Code, Notebooks, Daten bzw. Skripte zum Erzeugen)
- `presentation_group_XX.pdf`: Titel/Namen, Introduction, Materials & Methods,
  Results & Discussion, Conclusions, KI-Reflexion, **Anhang mit
  Punkte-Selbsteinschätzung inkl. Screenshots/Code**

Bekannte Widersprüche auf Moodle: «max. 16 points» vs. «max. 22 points» und
Abgabeslot «11 January 2026» vs. Titel «10.01.2027». Geplant wird mit 22 Punkten
und dem 10.01.2027.

## 4. Methodische Leitplanken

Die Forschungsfrage ist eine **Vergleichsfrage**: Ist der Wettereffekt auf
Verspätungen im Regionalverkehr *stärker* als im Fernverkehr? Daraus folgt:

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
- Datenbankzugriff nur über `src/db.py`.
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
| `/status` | Stand gegen Zeitplan und Bewertungsraster, nächste Schritte |
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
