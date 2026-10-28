---
description: Neues Notebook nach Konvention anlegen — /new-notebook <nn> <topic> <initials>
argument-hint: <nn> <topic> <initials>
---

Lege ein neues Jupyter-Notebook an. Argumente: $ARGUMENTS
(Nummer, Thema, Initialen, z. B. `03 eda_weather er`).

1. Fehlen Argumente, frag nach. Prüfe in `notebooks/`, ob die Nummer schon
   vergeben ist. Wenn ja, schlag die nächste freie vor.
2. Dateiname: `notebooks/NN_topic_initials.ipynb` (alles klein, Unterstriche).
3. Inhalt (gültiges nbformat 4, Python-3-Kernel):
   - Markdown-Zelle: Titel, Owner (Initialen), Datum, Zweck in einem Satz,
     Input (Tabellen oder Dateien), Output
   - Code-Zelle Setup:
     ```python
     import sys; sys.path.append("..")
     import pandas as pd
     import matplotlib.pyplot as plt
     import seaborn as sns
     from src.paths import RAW_DIR, PROCESSED_DIR
     from src.db import query, write_table, list_tables
     ```
   - Markdown-Zellen als Gliederung: `## 1. Load data`, `## 2. …`,
     `## Findings` (für die Folien), `## Open questions`
   - Am Schluss die Footer-Zelle aus der Kursvorlage (Markdown
     `### Jupyter notebook --footer info--`, darunter Code):
     ```python
     import os, platform
     from platform import python_version
     from datetime import datetime
     print('-----------------------------------')
     print(os.name.upper())
     print(platform.system(), '|', platform.release())
     print('Datetime:', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
     print('Python Version:', python_version())
     print('-----------------------------------')
     ```
4. Erinnere daran: Dieses Notebook gehört nur dieser Person. Gemeinsame
   Funktionen gehören nach `src/`.
