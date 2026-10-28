# Prompt library

Prompts for recurring tasks. In Claude Code, most of them exist as slash
commands. In claude.ai, copy the prompt.

## Start of a session
> Read docs/project-state.md. My initials are __. What is my next task according to the state, and what is the most important thing before then?

Claude Code: `/status`

## Load a new data source
> Use the data-pipeline agent: load ONE day of [source] as a sample into data/raw, show columns, data types, row count and 5 example rows. Don't build the full pipeline yet.

## Document a join
> I just joined [table A] with [table B] on [key]. Determine rows before/after and the lost records, and write the entry for docs/integration-log.md.

Claude Code: `/integration-log <step>`

## EDA
> Create an EDA for table [name] in my notebook [file]: descriptive statistics, missing values, distribution of the target variable per traffic type, and 3 plots that are relevant for the research question. For each plot one sentence: what does it show?

## Check a statistical test or model
> Use the stats-reviewer agent on [notebook/file]. Is the test or model suitable for our comparison question, and are the results interpreted correctly?

## Understand code or a method (for the video and the exam)
> Explain [file/function/method] so that I can explain it freely in the video. Ask me first what I already know.

Claude Code: `/explain <topic>`

## Log AI usage
> Write the line for docs/ai-log.md: I used [tool] for [task]. What went wrong / what I had to fix: [...]

Claude Code: `/ai-log <what>`

## Check the grading status
> Go through all grading criteria in CLAUDE.md and check what is demonstrably in the repo. Score range out of 22 points and the 3 measures with the biggest gain per effort.

Claude Code: `/check-grading`

## Rehearse a presentation
> Use the presentation-coach agent on [slides/script]. Expected grade per criterion, time per slide and per person, the 3 most important changes.

## End of a session
> Wrap up: AI log entry, integration log if needed, update project-state.md, check git status, propose a commit message.

Claude Code: `/session-end`
