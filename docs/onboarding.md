# Onboarding checklist

Goal: after this list you have the same state as everyone else. Takes about
60–90 min. Tick the boxes in your onboarding issue on GitHub.

## 1. Access
- [ ] Accept the GitHub invitation to `rexheeri/da-projekt-hs26`
- [ ] Tell the group your GitHub name ↔ real name (for `project-state.md`)

## 2. Install (skip what you already have)
- [ ] Git
- [ ] Python 3.10 or newer (3.12 recommended)
- [ ] VS Code with the extensions **Python** and **Jupyter** (VS Code suggests them when you open the repo)
- [ ] Claude Code (VS Code extension or CLI), *optional but recommended*
- [ ] Docker Desktop, *only needed for PostgreSQL, not before the presentation*

## 3. Set up the repo
```bash
git clone https://github.com/rexheeri/da-projekt-hs26.git
cd da-projekt-hs26
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.check_setup       # must end with "Setup OK."
```
- [ ] `check_setup` says **Setup OK**
- [ ] VS Code uses the `.venv` interpreter

## 4. Read (in this order, ~30 min)
- [ ] `README.md`: structure and team rules
- [ ] `docs/project-state.md`: current state, decisions, **the lecturer's answers**
- [ ] `docs/grading.md`: what is graded, how many points
- [ ] `docs/research-design.md`: research question, hypotheses, open decisions
- [ ] `docs/workplan.md`: phases, roles, dates
- [ ] `docs/concept-presentation.md`: what we present on 17.11.

## 5. Claude
- [ ] Read `docs/claude/README.md`
- [ ] Create your own `CLAUDE.local.md` (language, your role, your initials)
- [ ] Start Claude Code in the repo and run `/status`
- [ ] *Or* set up a claude.ai Project with `docs/claude/project-instructions.md`

## 6. First contribution (tests the Git workflow)
- [ ] `git pull`
- [ ] Fill in your row in `docs/project-state.md` (name, GitHub, initials, role)
- [ ] Commit (`Add <initials> to project state`) and `git push`

## 7. Dates in your calendar
- [ ] **Tue 17.11.2026, 11:00–12:45, SW301 Winterthur:** concept presentation,
  **attendance mandatory**. Take the morning off work now.
- [ ] **Sun 15.11.:** dry run (time to be agreed)
- [ ] **10.01.2027, 23:59:** final submission
- [ ] Weekly 15-min sync (day/time to be agreed)

## 8. Pick your first issue
- [ ] Assign yourself to the issues of your role in milestone **M1**
