# Grading

Source: Moodle course page (final project: as of 2026-10-06; concept
presentation: "Evaluation of the project concept presentation", as of
2026-10-28). Lecturer's answers of October 2026 included.
If Moodle changes, Moodle wins. Update this file and note it in the change log.

## Module grade

| Part | Weight | Date |
|---|---|---|
| Written exam (individual, open book, 60 min, 25–30 single choice) | 60 % | open |
| Concept presentation (group) | 20 % | **Tue 17.11.2026, 11:00–12:45, SW301**, on site, attendance mandatory |
| Final project (group) | 20 % | **10.01.2027, 23:59** |

---

## 1. Concept presentation (20 %)

- On site in Winterthur, at the beginning of the large class, from week 10.
  3–4 groups per lecture, **10 min per group**.
- Slide set as **PDF**, uploaded to Moodle.
- Content is the **concept**, not the finished project.

### Criteria (each graded 1–6, final grade = average of the 8)

| # | Criterion | The lecturer checks |
|---|---|---|
| 1 | **Structure & outline** | Clear outline presented and followed? Logical flow with recognizable thread? Balanced weighting of parts? Title clear? **Names of all students** available? |
| 2 | **Background & problem** | Context of the project clear? Problem convincingly motivated? |
| 3 | **Objective & research question** | Clearly defined? |
| 4 | **Data** | Source shown? **Structure of the data explained?** |
| 5 | **Methods** | Methods appropriate for the research question? Correctly described **and justified**? |
| 6 | **Expected results** | Plausible? **Linked back to the research question?** |
| 7 | **Language** | **Freely spoken?** |
| 8 | **Quality of the presentation** | Quality of graphics, tables & slides **according to scientific standards**? |

### Grading scale

| Grade | Meaning |
|---|---|
| 6 | Excellent: fulfilled completely and convincingly, without notable weaknesses |
| 5 | Good: fulfilled well, with only minor weaknesses |
| 4 | Sufficient: fulfilled in its essential aspects; basic requirements are met |
| 3 | Insufficient: key elements missing or incorrect |
| 2 | Poor: addressed only in fragments |
| 1 | Not fulfilled: not addressed / no performance shown |

What this means for us:
- Criteria 7 and 8 count as much as content. Reading from notes or slides
  costs a full criterion.
- Criterion 4 asks for the **structure**. Without real data (columns, types,
  rows, how sources connect) this is at most a 4.
- Criterion 6: "We expect X" is not enough. Each expected result must
  answer the research question or one hypothesis.
- ⚠ The Moodle text continues below the scale ("The final grade … is the average
  of these …"). The rest of the page is not captured yet.

---

## 2. Final project (20 %), max. 22 points

Lecturer confirmed: **max. 22 points** (9 + 6 + 7). The conversion to a grade
happens after all projects have been assessed, so it is **relative to the
other groups**.

### Minimum requirements (9 points)
- [ ] Own data collection via web scraping or web API (Kaggle not as main
  source). Confirmed: Ist-Daten **downloaded by script via the API** count.
- [ ] ≥ 2 sources integrated; integration documented: keys, joins,
  inconsistencies, records lost/gained → `docs/integration-log.md`
- [ ] Database + SQL from Python. Confirmed: **PostgreSQL replaces SQLite**.
- [ ] EDA, tabular **and** graphical
- [ ] Regression or classification with a research question beyond a standard
  prediction (comparison of groups/regions/periods/sources)
- [ ] Measures of fit
- [ ] Correct interpretation
- [ ] AI usage documented (pros, cons, where it failed) → `docs/ai-log.md`
- [ ] Material on Moodle

### Bonus (max. 6 points)
- [ ] Creativity
- [ ] PostgreSQL or similar instead of SQLite
- [ ] Geodata
- [ ] Chi², ANOVA or correlation with p-value
- [ ] Additionally k-means
- [ ] Public GitHub repo (URL on the slides)

### Video (max. 7 points)
- Length = number of persons × 5 min → **15 min** for us
- Graded: structure, topic, content, freely spoken, slides, AI reflection,
  time keeping
- **Do not scroll through notebooks.**

### Submission (one person for the group)
- `video_recording_group_XX.mp4` (in parts if necessary)
- `materials_group_XX.zip` (code, notebooks, data or scripts to rebuild it)
- `presentation_group_XX.pdf` with: title and names, Introduction, Materials &
  Methods, Results & Discussion, Conclusions, AI reflection, **appendix with
  self-assessment of points incl. screenshots/code**

Moodle inconsistency: submission slot says "Due: 11 January 2026", title says
"10.01.2027, 23:59" → we plan with 10.01.2027.
