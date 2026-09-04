<div align="center">

<h1>365 Bare-Metal C Concepts</h1>

<p>One concept a day. A growing journal of low-level programming knowledge.</p>

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://docs.github.com/en/actions)
[![YAML](https://img.shields.io/badge/YAML-CB171E?style=flat-square&logo=yaml&logoColor=white)](https://yaml.org/)
[![JSON](https://img.shields.io/badge/JSON-292929?style=flat-square&logo=json&logoColor=white)](https://www.json.org/)
[![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat-square&logo=markdown&logoColor=white)](https://github.github.com/gfm/)
![Study focus: Bare-Metal C](https://img.shields.io/badge/Study_Focus-Bare--Metal_C-00599C?style=flat-square&logo=c&logoColor=white)

[Overview](#overview) · [Project files](#project-files) · [Getting started](#getting-started) · [Example entry](#example-entry) · [Troubleshooting](#troubleshooting)

</div>

## Overview

**365 Bare-Metal C Concepts** is a daily study-journal automation designed for a 365-concept learning journey. A Python script reads an ordered JSON curriculum, appends the next unpublished concept to `DAILY_CONCEPTS.md`, and runs automatically through a cron schedule in GitHub Actions.

Each entry can include a summary, a core question, a checklist, an exercise, and space for personal notes. GitHub Actions commits the updated journal, building a version-controlled record over time.

The automation publishes the content supplied in JSON; studying, writing notes, and completing C exercises remain manual. C is the learning subject, while Python handles publishing. The workflow does not compile or flash firmware.

> [!NOTE]
> **365 is the curriculum target, not a hard-coded limit.** Supply 365 concepts for a 365-concept journal. The script accepts any non-empty concept list and stops adding entries when that list is exhausted.

## Features

- **Daily publishing:** Adds at most one new entry per date in the configured timezone.
- **Sequential progress:** Selects the first unused concept position in the JSON list.
- **Rerun protection:** Skips publication when today's date marker already exists.
- **Flexible content:** Accepts title-only strings or structured concept objects.
- **Study-friendly output:** Includes optional learning prompts and a manual notes section.
- **Simple persistence:** Stores publishing progress in Markdown comments without a database.
- **Manual testing:** Supports both local execution and the Actions tab's **Run workflow** button.

## Project files

Keep these files in the repository layout below; `DAILY_CONCEPTS.md` is created on the first successful publication.

| Path                                  | Technology            | Responsibility                                                           |
| ------------------------------------- | --------------------- | ------------------------------------------------------------------------ |
| `daily_concept.py`                    | Python                | Loads concepts, checks progress, and appends a journal entry.            |
| `concepts.json`                       | JSON                  | Stores the ordered curriculum and study prompts.                         |
| `.github/workflows/daily-concept.yml` | YAML / GitHub Actions | Defines the cron trigger, Python environment, and commit-and-push steps. |
| `DAILY_CONCEPTS.md`                   | Markdown              | Contains published entries, progress markers, and personal notes.        |
| `README.md`                           | Markdown              | Documents the project and its setup.                                     |

## How it works

1. A scheduled or manually dispatched workflow checks out the repository and sets up Python.
2. The script loads `concepts.json` and determines today's date using `Asia/Shanghai`.
3. If today's date marker is present, it exits without adding an entry. Otherwise, it finds the first unused **one-based list index**.
4. It appends that concept to the journal, keeping earlier entries and notes in place.
5. The workflow stages `DAILY_CONCEPTS.md`, commits only when there is a change, and pushes the commit.

The date is taken when the script executes, not from the planned cron time. Missed days are **not backfilled**: the next successful run publishes the next unused concept under its current date. Progress does not reset at the start of a new year.

> [!IMPORTANT]
> Preserve the `daily-concept-date` and `daily-concept-index` comments. Indices refer to list positions, not titles or permanent IDs. Once publishing begins, keep existing positions stable and append new concepts at the end; reordering or removing items can cause repeats or skipped topics. Duplicate titles at different positions are not filtered out.

## Getting started

You need a GitHub repository with Actions enabled and permission for the workflow to push journal updates. For local testing, use Python 3.13, matching the workflow below, and Git to synchronize changes.

### 1. Prepare the curriculum

Create `concepts.json` beside `daily_concept.py`. This one-concept example demonstrates the format; expand it with your own 365 entries:

```json
{
  "concepts": [
    {
      "title": "Bitwise Operations and Register Masks",
      "summary": "Study how bitwise operations manipulate individual bits.",
      "core_question": "How can you set, clear, and test a bit without changing unrelated bits?",
      "checks": [
        "Understand bit positions and masks.",
        "Compare AND, OR, XOR, and NOT operations."
      ],
      "exercise": "Use an unsigned integer as a simulated register and practice setting, clearing, and testing one bit."
    }
  ]
}
```

A top-level array is also accepted. Entries may be strings, such as `"Memory-Mapped I/O"`, or objects with these fields:

| Content       | Preferred key   | Accepted alternatives |
| ------------- | --------------- | --------------------- |
| Title         | `title`         | `name`, `concept`     |
| Summary       | `summary`       | `description`         |
| Core question | `core_question` | `question`            |
| Checklist     | `checks`        | `things_to_check`     |
| Exercise      | `exercise`      | `practice`            |

Use a non-empty title for each concept. Other fields are optional; empty sections are omitted. A checklist can be an array of strings or a single string. If multiple aliases are supplied, the first non-empty value in the order shown is used.

### 2. Add the Python publisher

Save the provided publishing script as `daily_concept.py` in the repository root. It uses `json`, `re`, `datetime`, `pathlib`, and `zoneinfo` from Python's standard library.

Replace the original backend-themed journal initialization inside `main()` with:

```python
journal = (
    "# Daily Bare-Metal C Concepts\n\n"
    "One bare-metal C study prompt is published automatically each day. "
    "My notes and implementations are added manually.\n"
)
```

Keep this inside the existing `else` block. If `DAILY_CONCEPTS.md` already exists, edit its heading and introductory text manually; changing this template only affects a newly created journal.

### 3. Configure GitHub Actions

Create `.github/workflows/daily-concept.yml` with the following configuration. It preserves the supplied publishing logic and uses bare-metal C naming throughout.

```yaml
name: Publish daily bare-metal C concept

on:
  schedule:
    # Every day at 05:00am in Asia/Shanghai
    - cron: "0 21 * * *"
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: daily-bare-metal-c-concept
  cancel-in-progress: false

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.13"

      - name: Publish today's concept
        run: python daily_concept.py

      - name: Commit and push
        shell: bash
        run: |
          git config user.name "$GITHUB_ACTOR"
          git config user.email "${GITHUB_ACTOR_ID}+${GITHUB_ACTOR}@users.noreply.github.com"

          git add DAILY_CONCEPTS.md

          if git diff --cached --quiet; then
            echo "Nothing new to commit."
            exit 0
          fi

          git commit -m "docs: publish daily bare-metal C concept"
          git push
```

The action references follow the official [checkout](https://github.com/actions/checkout) and [setup-python](https://github.com/actions/setup-python) documentation. The concurrency group prevents overlapping runs of this workflow; it does not coordinate local edits or other workflows.

The cron expression requests **05:00 every day in `Asia/Shanghai` (UTC+8)**. Keep the YAML `timezone` and Python's `TIMEZONE = ZoneInfo("Asia/Shanghai")` aligned if you change the timezone. GitHub supports the timezone field and uses UTC when it is omitted. See [scheduled workflow documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

> [!IMPORTANT]
> Add the Python script, JSON curriculum, and workflow to the repository's **default branch**—`main` if that is your default—using its normal commit or pull-request process. Scheduled workflows run only from the default branch. Scheduling is best-effort: runs can be delayed or dropped, and public-repository schedules can be disabled after 60 days without repository activity. See [GitHub's scheduling limitations](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

The workflow uses GitHub's built-in token through checkout and requests `contents: write` for publishing. No personal access token needs to be added for a repository that allows these workflow pushes. Repository and organization policies still apply; if direct pushes are prohibited, use an approved pull-request publishing process instead of weakening branch protections.

### 4. Test the publisher

From the repository root, validate the JSON and run the script:

```bash
python -m json.tool concepts.json
python daily_concept.py
```

Use `python3` if that is your interpreter command. No additional Python packages are needed when system timezone data is available. On Windows or systems without it, install the timezone data package with `python -m pip install tzdata`. See [Python's timezone data requirements](https://docs.python.org/3.13/library/zoneinfo.html#data-sources).

Local execution updates the journal but does not commit or push it. Synchronize your clone and save intended changes through your normal Git workflow.

To test on GitHub after the required files are on the default branch:

1. Open **Actions** and select **Publish daily bare-metal C concept**.
2. Select **Run workflow**, choose the default branch, and start the run.
3. Check the run's logs and successful completion status.
4. Open `DAILY_CONCEPTS.md` to inspect the published entry.
5. Run it again on the same local date. Expect `An entry already exists for YYYY-MM-DD` and no additional publication commit.

A successful run can produce no commit if today's entry already exists or the curriculum is exhausted. After the final concept, the script prints `Every concept has already been published`; the workflow itself remains scheduled until you disable or change it.

## Example entry

The sample concept above produces an entry like this; the date reflects the actual execution day:

```markdown
<!-- daily-concept-date: 2026-09-04 -->
<!-- daily-concept-index: 1 -->

## 2026-09-04 — Bitwise Operations and Register Masks

Study how bitwise operations manipulate individual bits.

**Core question:** How can you set, clear, and test a bit without changing unrelated bits?

**Things to check:**

- Understand bit positions and masks.
- Compare AND, OR, XOR, and NOT operations.

**Exercise:** Use an unsigned integer as a simulated register and practice setting, clearing, and testing one bit.

**My notes:**

-
```

Replace the empty notes bullet with your explanation, observations, or links to practice code. New entries are appended below earlier entries.

## Troubleshooting

| Symptom                                  | What to check                                                                                                                                                                                |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `concepts.json was not found`            | Place the file beside `daily_concept.py`; paths are resolved relative to the script.                                                                                                         |
| JSON parsing or concept validation error | Check JSON syntax, ensure the list is non-empty, and provide a title for every object.                                                                                                       |
| `ZoneInfoNotFoundError`                  | Install `tzdata` in the Python environment used to run the script.                                                                                                                           |
| Successful run but no new entry          | Inspect the logs for an existing date marker or an exhausted list.                                                                                                                           |
| Schedule does not run                    | Confirm Actions is enabled, the workflow is on the default branch, and its schedule has not been disabled; scheduled runs may also be delayed.                                               |
| Commit or push rejected                  | Check token permissions and branch rules. If the branch advanced during the run, rerun against its latest state after reviewing any competing edits; do not force-push over journal changes. |

> [!TIP]
> Treat publishing as a study prompt, not proof of completion: read the concept, attempt the exercise, and explain what you learned in your own notes.
