# Konzeptpräsentation DA – Checkliste und Raster

Stand 03.11.2026 · ER. Teamversion der Checkliste, ergänzt `docs/concept-presentation.md`. Foliengerüst: `presentation/concept_presentation_group_03.pptx` (Konzept pro Folie in den Sprechernotizen, rot = noch nachzutragen).

## Eckdaten

Wir präsentieren das **Konzept, nicht Resultate**: 10 Minuten, live vor Ort, bewertet mit 8 gleich gewichteten Kriterien. Zwei davon (frei gesprochen, Folienqualität) sind reine Form und machen zusammen 25 % der Präsentationsnote aus.

| Punkt | Stand |
| --- | --- |
| Termin | Di 17.11.2026, 11:00, am Anfang der Grossklasse (Slot 11:00–12:45) |
| Ort | SW301, Winterthur |
| Dauer | 10 Min. pro Gruppe, 3–4 Gruppen pro Vorlesung |
| Präsenz | Pflicht vor Ort für alle drei, nur an diesem Tag |
| Sprache | Englisch (Unterrichts- und Abgabesprache) |
| Inhalt laut Modul | Background, Problem, Ziele, Forschungsfrage, Daten, Methoden, erwartete Resultate |
| Folien | Als PDF auf Moodle hochladen; der Slot nennt die Frist 10.01.2027, 23:59. Wir laden direkt nach dem 17.11. hoch. |
| Gewicht | 20 % der Modulnote |
| Bewertung | 8 Kriterien, je Note 1–6, Durchschnitt = Präsentationsnote |
| Nebeneffekt | Gellrich gibt das Thema hier formell frei |
| Aufnahme | Für die Konzeptpräsentation nicht verlangt (das Video gehört zum Schlussprojekt) |

Notenskala je Kriterium: 6 vollständig und überzeugend · 5 gut, kleine Schwächen · 4 im Wesentlichen erfüllt · 3 zentrale Elemente fehlen oder falsch · 2 nur fragmentarisch · 1 nicht erfüllt.

## Bewertungsraster: was pro Kriterium rein muss

Jedes Kriterium zählt 12,5 %. Die Spalte «Moodle prüft» ist der Originalwortlaut, die Spalte daneben übersetzt ihn in konkrete Folieninhalte für unser Thema.

| # | Kriterium | Moodle prüft | Muss konkret auf die Folien | Folie |
| --- | --- | --- | --- | --- |
| 1 | Structure & outline | Gliederung gezeigt und eingehalten? Roter Faden? Teile ausgewogen? Titel klar? Namen aller Studierenden? | Titel als Frage oder Aussage, alle drei Namen, Modul, Datum · Gliederung mit 5–6 Punkten, die wir exakt so abarbeiten · Foliennummern · Zeit pro Teil ungefähr gleich | 1, 2, 12 |
| 2 | Background & problem | Kontext klar? Problem überzeugend motiviert? | Warum Pünktlichkeit zählt (Pendler, SBB-Definition «< 3 Min.» mit Quelle) · Zürich als Knoten · Wetter als bekannter Störfaktor · die Lücke: Reagiert der Regionalverkehr stärker als der Fernverkehr? · wem die Antwort nützt (Fahrplanreserven, Kundeninformation) | 3, 4 |
| 3 | Objective & research question | Klar definiert? | Forschungsfrage wörtlich · Ziel in einem Satz · Abgrenzung: Region, Zeitraum, nur Bahn · Hypothesen H1–H3 als H0/H1, α = 0.05 | 5, 6 |
| 4 | Data | Quelle gezeigt? Struktur der Daten erklärt? | Drei Quellen mit Name und URL (Ist-Daten, MeteoSchweiz STAC, Haltestellenverzeichnis) · Zugriff per Skript/API · Zeitraum und Volumen · **echte Stichprobe**: Schlüsselspalten mit Typ, Zeilenzahlen · wie die Quellen zusammenhängen (Haltestelle → nächste Station → Stunde) als ER-Skizze · PostgreSQL | 7, 8 |
| 5 | Methods | Passend zur Forschungsfrage? Korrekt beschrieben und begründet? | Pipeline-Diagramm API → DB → EDA → Tests → Klassifikation · pro Methode ein Satz *warum*: Chi² je Verkehrsart, Differenz der Verspätungsquoten (Kern der Vergleichsfrage), Classification Tree und Random Forest mit und ohne Wetter, Recall/ROC-AUC wegen Klassenungleichgewicht · Kontrollvariablen (Stunde, Wochentag) · wie wir die mitgebrachte Verspätung des Fernverkehrs behandeln | 9 |
| 6 | Expected results | Plausibel? Zurück auf die Forschungsfrage bezogen? | Pro Hypothese: was wir erwarten und warum · ausdrücklicher Bezug zur Forschungsfrage · mögliches Gegenresultat · ein bis zwei Limitationen (Korrelation ≠ Kausalität, nächste Station ≠ Wetter auf der Strecke) | 10, 11 |
| 7 | Language | Frei gesprochen? | Kein Ablesen von Folie oder Papier, höchstens Stichwortkarten · saubere Übergabe zwischen den Sprechern · jeder übt seinen Teil mindestens 3× laut | alle |
| 8 | Quality of the presentation | Grafiken, Tabellen, Folien nach wissenschaftlichem Standard? | Folientitel = Aussage · jede Grafik mit Achsen, Einheiten, n und Quelle · Quellen auf der Folie, Liste am Schluss · Regional und Fernverkehr immer in derselben Farbe · Schrift ≥ 18 pt · keine ganzen Sätze | alle |

Kriterium 4 ist der Grund, warum wir bis zum 17.11. echte Stichprobendaten brauchen. Ohne sie bleibt «Struktur der Daten erklärt» eine Behauptung.

## Folienplan

12 Folien, Ziel 9:30–9:50, gut 3:15 pro Person. Basis ist `docs/concept-presentation.md`, ergänzt um die Behandlung des Fernverkehr-Bias auf Folie 9. Die Sprecher 1–3 werden im Teamcall zugeteilt.

| # | Folie | Inhalt | Kriterium | Zeit | Sprecher |
| --- | --- | --- | --- | --- | --- |
| 1 | Title | Titel als Frage oder Aussage, alle drei Namen, Modul, Datum | 1 | 0:15 | 1 |
| 2 | Outline | 5–6 Punkte, genau so abgearbeitet | 1 | 0:15 | 1 |
| 3 | Background | Pünktlichkeit, SBB-Definition 3 Min. (Quelle), Zürich als Knoten, Wetter als Störfaktor | 2 | 0:50 | 1 |
| 4 | Problem | Lücke: Ist der Regionalverkehr wetteranfälliger? Warum das zählt | 2 | 0:40 | 1 |
| 5 | Objective & RQ | Forschungsfrage wörtlich, Ziel in einem Satz, Abgrenzung | 3 | 0:40 | 2 |
| 6 | Hypotheses | H1–H3 als H0/H1, α = 0.05 | 3, 5 | 0:50 | 2 |
| 7 | Data sources | 3 Quellen mit URL, Zugriff per Skript/API, Zeitraum, Volumen | 4 | 0:45 | 2 |
| 8 | Data structure | Echte Stichprobe: Spalten, Typen, Zeilen, ER-Skizze, Join-Logik | 4 | 1:15 | 2 |
| 9 | Methods | Pipeline-Diagramm, je Methode ein *warum*, Kontrollvariablen, Umgang mit mitgebrachter Verspätung | 5 | 1:20 | 3 |
| 10 | First look *(preliminary)* | Eine Grafik: Verspätungsquote je Verkehrsart × trocken/Regen/Schnee, «preliminary, n = …» | 4, 6 | 0:45 | 3 |
| 11 | Expected results | Pro Hypothese Erwartung und Begründung, Bezug zur RQ, Limitation | 6 | 0:55 | 3 |
| 12 | Next steps | Zeitplan bis 10.01., GitHub-URL | 1 | 0:20 | 3 |
|  | **Total** |  |  | **~9:50** |  |

Folie 10 ist optional. Fehlen bis 12.11. belastbare Zahlen, fällt sie weg und Folie 8 bekommt die Zeit.

## Pflichtelemente und Formalien

Abhaken, bevor das PDF als fertig gilt.

**Inhalt**

- [ ] Titel und **alle drei Namen** auf Folie 1
- [ ] Gliederung auf Folie 2, Reihenfolge der Folien stimmt damit überein
- [ ] Forschungsfrage wörtlich, identisch auf Folie 5 und Folie 11
- [ ] Alle drei Datenquellen mit Name, URL und Zugriffsart
- [ ] Echte Datenstruktur: Spalten, Typen, Zeilenzahlen aus der Stichprobe
- [ ] Join-Logik sichtbar (Haltestelle → nächste Wetterstation → Stunde)
- [ ] Jede Methode mit einem Satz Begründung
- [ ] Erwartete Resultate je Hypothese, mit Bezug zur Forschungsfrage
- [ ] Mindestens eine Limitation genannt
- [ ] GitHub-URL auf der letzten Folie

**Form**

- [ ] Foliennummern auf jeder Folie
- [ ] Folientitel formulieren die Aussage, nicht das Thema
- [ ] Jede Grafik: Titel, Achsen mit Einheit, n, Quelle
- [ ] Jede fremde Zahl mit Quelle auf der Folie, Quellenliste am Schluss
- [ ] Regional- und Fernverkehr überall in denselben zwei Farben
- [ ] Schrift mindestens 18 pt, keine ganzen Sätze
- [ ] Englisch durchgehend, Begriffe einheitlich («regional», «long-distance»)
- [ ] PDF exportiert, Dateiname mit Gruppe 03

**Vortrag**

- [ ] Gesamtzeit im Probelauf höchstens 10:00
- [ ] Jeder spricht frei, höchstens Stichwortkarten
- [ ] Übergaben zwischen den Sprechern eingeübt

## Was nicht hineingehört

- **Fertige Resultate oder Schlussfolgerungen.** Bewertet wird das Konzept. Vorläufige Zahlen nur als «preliminary» mit n.
- **Code und Notebooks.** Kein Code-Screenshot, ausser er erklärt die Datenstruktur besser als eine Tabelle.
- **Modellnamen ohne Begründung.** «Random Forest» allein ist kein Methodenteil, das *warum* gibt die Note.
- **Textfolien zum Ablesen.** Sie kosten Kriterium 7 und 8 gleichzeitig.
- **Behauptungen ohne Quelle**, etwa die SBB-Definition der Pünktlichkeit.
- **Mehr als 12 Folien.** Bei 10 Minuten geht jede zusätzliche Folie von der Zeit für Daten und Methoden ab.

## Kritische Fragen mit Antwortstichworten

Gellrich gibt das Thema an der Präsentation formell frei. Diese Fragen sind am wahrscheinlichsten. Jeder kennt die Antworten zu seinem Teil.

| Frage | Antwortstichworte |
| --- | --- |
| Warum genau 3 Minuten? | SBB-Definition der Kundenpünktlichkeit (Quelle zeigen), binäres Ziel für die Klassifikation |
| Ist der Archiv-Download eigene Datenerhebung? | Gellrich hat den Skript-Download der Tagesdateien als eigene Erhebung bestätigt; die Winterdaten liegen im offiziellen Monatsarchiv und werden ebenfalls per Skript geholt. Vorher kurz mit ihm klären |
| Der Fernverkehr bringt Verspätung von ausserhalb mit. Verzerrt das nicht? | Ja, darum messen wir zusätzlich die Verspätungszunahme im Studiengebiet bzw. kontrollieren die Verspätung bei Einfahrt in die Region |
| Wie unterscheidet ihr Regen und Schnee? | Niederschlag bei Temperatur ≤ 0 °C als Schnee, geprüft gegen die Zunahme der Schneehöhe; Schneeregen um 0 °C als Limitation |
| Wohin gehört der IR? | Entscheid im Team mit Begründung (offener DECIDE-Punkt) |
| Gab es überhaupt genug Schneetage? | Studienzeitraum wurde aus den Wetterdaten gewählt, Anzahl Schneetage zeigen |
| Warum Klassifikation, wenn ihr einen Vergleich wollt? | Kernantwort ist der Effektvergleich (Differenz der Verspätungsquoten); das Modell ergänzt: AUC-Gewinn durch Wettervariablen je Verkehrsart |
| Accuracy ist bei seltenen Verspätungen wertlos. | Darum Recall, Precision und ROC-AUC, Baseline = Anteil der Mehrheitsklasse |
| Bei Millionen Zeilen ist alles signifikant. | Effektgrössen und Konfidenzintervalle zählen mehr als p-Werte; H3 auf Tagesebene |
| Ist das nicht nur der Berufsverkehr? | Stunde, Wochentag und Ferien als Kontrollvariablen |
| Wie gross sind die Daten? | Zeilen roh und gefiltert, Speicherbedarf, Zeitraum aus der Pipeline |
| Nächste Wetterstation = Wetter auf der Strecke? | Nein, Distanzen zeigen (Median, Maximum), als Limitation nennen |

## Vorbereitung bis 17.11.

ER ist vom 07. bis 15.11. nicht verfügbar. Deshalb verschiebt sich der Probelauf auf Mo 16.11., und LS und LK tragen den Folienentwurf.

- [ ] Bis Do 05.11.: Teamcall, Rollen und Sprecher 1–3 zugeteilt
- [ ] Bis Fr 06.11.: Stichprobendaten in der DB, DECIDE-Punkte entschieden, Methodenteil (Folien 6, 9, 11) als Entwurf
- [ ] Bis Do 12.11.: Folienentwurf komplett, Grafik für Folie 10 oder Entscheid, sie wegzulassen
- [ ] So 15.11.: Review mit dem `presentation-coach`-Agenten
- [ ] Mo 16.11.: Probelauf mit Stoppuhr, alle drei, höchstens 10:00, danach Folien korrigieren
- [ ] Vormittag 17.11. bei der Arbeit frei genommen (alle drei)
- [ ] Am 17.11. dabei: Laptop, Adapter, PDF auf USB-Stick als Reserve
- [ ] Nach der Präsentation: PDF auf Moodle hochladen, Feedback in `docs/project-state.md` eintragen
