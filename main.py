import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_DIRECTORY = Path(__file__).resolve().parent
CONCEPTS_FILE = BASE_DIRECTORY / "concepts.json"
JOURNAL_FILE = BASE_DIRECTORY / "DAILY_CONCEPTS.md"
TIMEZONE = ZoneInfo("Asia/Shanghai")


def load_concepts():
    if not CONCEPTS_FILE.exists():
        raise FileNotFoundError("concepts.json was not found")

    data = json.loads(CONCEPTS_FILE.read_text(encoding="utf-8"))

    # Support {"concepts": [...]}
    if isinstance(data, dict):
        data = data.get("concepts")

    if not isinstance(data, list) or not data:
        raise ValueError(
            "concepts.json must contain a non-empty list "
            "or an object with a 'concepts' list"
        )

    return data


def normalize_concept(item):
    if isinstance(item, str):
        return {
            "title": item.strip(),
            "summary": "",
            "question": "",
            "checks": [],
            "exercise": "",
        }

    if not isinstance(item, dict):
        raise ValueError("Each concept must be a string or JSON object")

    title = item.get("title") or item.get("name") or item.get("concept")

    if not title:
        raise ValueError("A concept object is missing its title")

    checks = item.get("checks") or item.get("things_to_check") or []

    if isinstance(checks, str):
        checks = [checks]

    return {
        "title": str(title).strip(),
        "summary": str(item.get("summary") or item.get("description") or "").strip(),
        "question": str(
            item.get("core_question") or item.get("question") or ""
        ).strip(),
        "checks": [str(check).strip() for check in checks if str(check).strip()],
        "exercise": str(item.get("exercise") or item.get("practice") or "").strip(),
    }


def build_entry(date, index, concept):
    lines = [
        "",
        f"<!-- daily-concept-date: {date} -->",
        f"<!-- daily-concept-index: {index} -->",
        f"## {date} — {concept['title']}",
        "",
    ]

    if concept["summary"]:
        lines.extend(
            [
                concept["summary"],
                "",
            ]
        )

    if concept["question"]:
        lines.extend(
            [
                f"**Core question:** {concept['question']}",
                "",
            ]
        )

    if concept["checks"]:
        lines.extend(
            [
                "**Things to check:**",
                "",
            ]
        )

        lines.extend(f"- {check}" for check in concept["checks"])
        lines.append("")

    if concept["exercise"]:
        lines.extend(
            [
                f"**Exercise:** {concept['exercise']}",
                "",
            ]
        )

    lines.extend(
        [
            "**My notes:**",
            "",
            "- ",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    concepts = load_concepts()
    today = datetime.now(TIMEZONE).date().isoformat()

    if JOURNAL_FILE.exists():
        journal = JOURNAL_FILE.read_text(encoding="utf-8")
    else:
        journal = (
            "# Daily Backend Concepts\n\n"
            "One backend-engineering study prompt is published automatically "
            "each day. My notes and implementations are added manually.\n"
        )

    date_marker = f"<!-- daily-concept-date: {today} -->"

    # Prevent multiple entries when the workflow is rerun on the same day.
    if date_marker in journal:
        print(f"An entry already exists for {today}")
        return

    used_indices = {
        int(value)
        for value in re.findall(
            r"<!-- daily-concept-index: (\d+) -->",
            journal,
        )
    }

    selected_index = None
    selected_concept = None

    for index, item in enumerate(concepts, start=1):
        if index not in used_indices:
            selected_index = index
            selected_concept = normalize_concept(item)
            break

    if selected_concept is None:
        print("Every concept has already been published")
        return

    entry = build_entry(
        today,
        selected_index,
        selected_concept,
    )

    updated_journal = journal.rstrip() + "\n" + entry
    JOURNAL_FILE.write_text(updated_journal, encoding="utf-8")

    print(f"Published concept {selected_index}: " f"{selected_concept['title']}")


if __name__ == "__main__":
    main()
