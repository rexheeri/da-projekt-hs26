"""Create labels, milestones and issues on GitHub from tools/issue_list.py.

Requires the GitHub CLI, logged in once:
    winget install --id GitHub.cli      (then open a new terminal)
    gh auth login

Run from the repo root:
    python tools/create_issues.py --dry-run     # shows what would happen
    python tools/create_issues.py               # creates everything

Safe to run again: existing labels are updated, existing milestones and
issues (same title) are skipped.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Make tools/ importable so we can load the issue definitions next to this file
sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue_list import ISSUES, LABELS, MILESTONES  # noqa: E402

REPO = "rexheeri/da-projekt-hs26"
DRY_RUN = "--dry-run" in sys.argv  # with --dry-run nothing is sent to GitHub


def gh(*args, check=True):
    """Run a gh command and return its stdout. Stops the script on errors."""
    # encoding="utf-8": issue texts contain umlauts and emoji, Windows would default to cp1252
    result = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode != 0:
        sys.exit(f"gh {' '.join(args[:3])} … failed:\n{result.stderr}")
    return result.stdout


def main():
    """Create labels, then milestones, then issues (issues need both to exist)."""
    # Preconditions: gh installed and logged in
    if shutil.which("gh") is None:
        sys.exit("GitHub CLI not found. Install: winget install --id GitHub.cli, then gh auth login")
    if not DRY_RUN and subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        sys.exit("Not logged in. Run: gh auth login")

    print(f"Repository: {REPO}{'  (DRY RUN)' if DRY_RUN else ''}\n")

    # 1. Labels: --force updates colour/description if the label already exists
    print("Labels")
    for name, color, description in LABELS:
        print(f"  {name}")
        if not DRY_RUN:
            gh("label", "create", name, "--color", color, "--description", description, "--force", "-R", REPO)

    # 2. Milestones: gh has no milestone command, so we use the REST API via "gh api"
    print("\nMilestones")
    existing_ms = set()
    if not DRY_RUN:
        existing_ms = {m["title"] for m in json.loads(gh("api", f"repos/{REPO}/milestones?state=all&per_page=100"))}
    for m in MILESTONES:
        if m["title"] in existing_ms:
            print(f"  skip (exists): {m['title']}")
            continue
        print(f"  create: {m['title']}")
        if not DRY_RUN:
            gh("api", "-X", "POST", f"repos/{REPO}/milestones",
               "-f", f"title={m['title']}", "-f", f"due_on={m['due_on']}", "-f", f"description={m['description']}")

    # 3. Issues: skip titles that already exist (open or closed) to avoid duplicates
    print("\nIssues")
    existing = set()
    if not DRY_RUN:
        existing = {i["title"] for i in json.loads(gh("issue", "list", "-R", REPO, "--state", "all", "--limit", "500", "--json", "title"))}
    created = 0
    for issue in ISSUES:
        if issue["title"] in existing:
            print(f"  skip (exists): {issue['title']}")
            continue
        print(f"  create: [{issue['milestone'][:2]}] {issue['title']}")
        if not DRY_RUN:
            args = ["issue", "create", "-R", REPO, "--title", issue["title"], "--body", issue["body"],
                    "--milestone", issue["milestone"]]
            # one --label flag per label
            for label in issue["labels"]:
                args += ["--label", label]
            gh(*args)
        created += 1

    print(f"\nDone. {created} issue(s) {'would be ' if DRY_RUN else ''}created.")


if __name__ == "__main__":
    main()
