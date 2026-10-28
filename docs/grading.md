# Grading

Source: full text of the Moodle course page "Data Analytics (2026-HS)",
captured 2026-10-28, plus the lecturer's email answers of October 2026.
If Moodle changes, Moodle wins. Update this file and note it in the change log.

## Module grade

| Part | Weight | Date |
|---|---|---|
| Written exam (individual, open book, 60 min, single choice with 4 options, covers the **entire** module) | 60 % | open |
| Concept presentation (group) | 20 % | **Tue 17.11.2026, 11:00–12:45, SW301**, on site, attendance mandatory |
| Final project submission (group) | 20 % | **10.01.2027, 23:59** |

---

## 1. Concept presentation (20 %)

- On site in Winterthur, at the beginning of the large class, from week 10.
  3–4 groups per lecture, **10 min per group**.
- Slide set as **PDF**, uploaded to Moodle ("Submission of the presentation
  (PDF-document) of the project concept", due 10.01.2027 23:59; we upload right
  after 17.11.).
- Content is the **concept**, not the finished project. The topic is
  formally approved at this presentation.

### Criteria (each graded 1–6 independently, final grade = average of the 8)

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

---

## 2. Final project (20 %), max. 22 points

Max. **22 points** (9 + 6 + 7), confirmed by the lecturer. The Moodle course
index (left navigation) still says "Project evaluation (max. 16 points)". The
section itself says 22. The grade conversion happens after all projects have
been assessed, so it is **relative to the other groups**.

### Minimum requirements (9 points)
The project must be a Data Analytics project and integrate several module
topics, at a minimum:
- [ ] **Data collection** via web scraping and/or web API, **by the group
  itself**. Ready-made datasets (e.g. Kaggle) are not allowed as the primary
  source. Confirmed: Ist-Daten **downloaded by script via the API** count.
- [ ] **Data preparation and integration:** data from ≥ 2 different sources
  combined. The integration step must be documented: matching keys, joining,
  resolving inconsistencies, records lost/gained → `docs/integration-log.md`
- [ ] **Data storage** in a database **with SQL queries from within Python**.
  Moodle says SQLite. Confirmed: **PostgreSQL replaces SQLite**.
- [ ] **Rich** non-graphical **and** graphical EDA
- [ ] **Modeling:** regression or classification. The research question must go
  beyond a standard prediction task (comparison between groups, regions,
  time periods or data sources). Ours: regional vs. long-distance.
- [ ] **Model evaluation** with suitable measures of fit (accuracy, recall,
  precision, …)
- [ ] **Correct interpretation** of model results and measures of fit
- [ ] **Documentation of AI usage for creating the code *and the presentation*:**
  advantages, disadvantages, where something did not work → `docs/ai-log.md`
- [ ] **Material on Moodle (data, Jupyter notebooks, …)**

Overused standard topics (e.g. plain price prediction) are graded lower on
creativity. That does not apply to us.

### Bonus (max. 6 points)
- [ ] **Creativity of implementation:** "anything not specified in the lessons
  and exercises". Our candidates: z-test on the difference of risk
  differences, AUC gain from weather features, delay increase between stops,
  automated API pipeline.
- [ ] **PostgreSQL** or similar (no SQLite!) **with e.g. SQL joins and
  aggregations from within Python**. The joins and aggregations must
  happen in SQL, not only in pandas.
- [ ] **Geographical data**, integrated **and** visualized
- [ ] **Chi², ANOVA or correlation**, each with a p-value
- [ ] **k-means** in addition to the classification model
- [ ] **Public GitHub repo**, URL in the project presentation

### Video (max. 7 points)
Length = number of students × 5 min → **15 min** for us.

Criteria:
1. Structure & outline
2. Topic presentation (topic clearly defined? how convincingly presented?)
3. Content (substance, depth, weighting of parts)
4. Language / auxiliary tools (freely spoken?)
5. Quality of the presentation & slides
6. **Reflection on AI usage**, in **slides and video**: which AI tools, how, advantages,
   disadvantages, where something did not work
7. Time keeping

Lecturer's notes:
- Use the slide set (PDF) as the basis for the video.
- Show Python code and live demos **only if it improves understanding** of methods and results.
- **Do not just scroll** through notebooks without explaining code and results.
- "AI is a tool, not a substitute for understanding. The evaluation focuses on
  your ability to **explain and justify** your data, methods, and results."

### Submission (on Moodle, group number **3**, by one student)
- `video_recording_group_03.mp4`. If too large for Moodle, split it:
  `video_recording_group_03_part_1.mp4`, …
- `materials_group_03.zip` with **all data** and the Jupyter notebooks.
  The data must be included, so plan a compact export (see work plan).
- `presentation_group_03.pdf`, minimal structure:
  1. Title and **full name** of each student
  2. Introduction: background, problem, objective, research question
  3. Materials and methods: data collection method, content of data, EDA
     methods, modelling methods
  4. Results & Discussion
  5. Conclusions
  6. Reflection on AI usage: tools, tasks, advantages, disadvantages, what did not work
  7. **Appendix: what we did to earn each point, with screenshots and code
     snippets.** The lecturer makes the final call, not only based on our list.

Moodle inconsistency: the final-project slot says "Due: Sunday, 11 January
2026", its title says "10.01.2027, 23:59". We plan with 10.01.2027.
