"""
Preflight check for the Alpine Ski House guest feedback lab (Lab A).

Each task in this lab can be completed on its own. Before you start a task,
run this script to confirm your .env file has everything that task needs.

Run it from the starter code folder - Labfiles/A-analyze-and-translate-text/Python -
which is the folder you opened in VS Code and where your terminal is already open:

    python ../setup/check_env.py --task 2

(If you run it from the lab root instead, drop the '../' and use
'python setup/check_env.py --task 2'. Note that this script is NOT reachable from
Solution/Python, because there is no Solution/setup folder.)

It never changes anything - it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (code)   FOUNDRY_ENDPOINT
    Task 2  (code)   TRANSLATOR_ENDPOINT
    Task 3  (code)   PROJECT_ENDPOINT, AGENT_NAME
"""

import argparse
import os
from pathlib import Path

try:
    from dotenv import dotenv_values
except ModuleNotFoundError:
    # python-dotenv is installed into the lab's virtual environment, but this
    # preflight check is meant to run BEFORE you install anything - and from a
    # terminal where labenv may not be activated. Fall back to a small stdlib
    # parser so the check always works.
    def dotenv_values(env_path):
        """Minimal .env reader: KEY=VALUE, ignoring blanks and # comments."""
        values = {}
        try:
            # utf-8-sig so a BOM-prefixed .env parses cleanly too.
            with open(env_path, encoding="utf-8-sig") as handle:
                lines = handle.readlines()
        except OSError:
            return values
        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].lstrip()
            key, separator, value = line.partition("=")
            if not separator:
                continue
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            else:
                # Strip an unquoted trailing comment, as python-dotenv does.
                comment = value.find(" #")
                if comment != -1:
                    value = value[:comment].rstrip()
            values[key] = value
        return values

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: ["FOUNDRY_ENDPOINT"],
    2: ["TRANSLATOR_ENDPOINT"],
    3: ["PROJECT_ENDPOINT", "AGENT_NAME"],
}

ALL_KEYS = ("FOUNDRY_ENDPOINT", "TRANSLATOR_ENDPOINT", "PROJECT_ENDPOINT", "AGENT_NAME")

# Placeholder text shipped in .env.example - present but not yet filled in.
PLACEHOLDERS = {
    "",
    "your_foundry_endpoint",
    "your_translator_endpoint",
    "your_project_endpoint",
    "<your_foundry_endpoint>",
    "<your_translator_endpoint>",
    "<your_project_endpoint>",
}

# How to fix each key, shown only when it's missing.
FIX_HINTS = {
    "FOUNDRY_ENDPOINT": (
        "Copy the project endpoint from the Microsoft Foundry portal and remove the "
        "'/api/projects/{project_name}' suffix, so it ends at the .com domain. "
        "It should look like https://your-resource.services.ai.azure.com"
    ),
    "TRANSLATOR_ENDPOINT": (
        "Azure Translator uses the Azure AI services form of your Foundry resource "
        "endpoint. It should look like "
        "https://your-resource.cognitiveservices.azure.com/"
    ),
    "PROJECT_ENDPOINT": (
        "Task 3 uses the full project endpoint, including the "
        "'/api/projects/{project_name}' suffix. Copy it from the project overview "
        "page in the Microsoft Foundry portal."
    ),
    "AGENT_NAME": (
        "Task 3 needs the agent you create in the Foundry portal. Set "
        "AGENT_NAME=guest-feedback-agent (the name is case-sensitive)."
    ),
}


def find_env_file():
    """Return the .env next to the lab's Python folder, wherever this is run from."""
    here = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / ".env",
        here.parent / "Python" / ".env",
        here.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Default to the Python-folder location even if it doesn't exist yet.
    return here.parent / "Python" / ".env"


def load_values(env_path):
    """Merge real environment variables over .env file values (env wins)."""
    values = {}
    if env_path.exists():
        values.update({k: v for k, v in dotenv_values(env_path).items() if v is not None})
    for key in ALL_KEYS:
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def is_set(values, key):
    """A key counts as set if it's present and not a leftover placeholder."""
    value = (values.get(key) or "").strip()
    return bool(value) and value not in PLACEHOLDERS


def main():
    parser = argparse.ArgumentParser(
        description="Check that your .env has what a given lab task needs."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(TASK_REQUIREMENTS),
        required=True,
        help="Which task you're about to start (1-3).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    required = TASK_REQUIREMENTS[args.task]

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    missing = [key for key in required if not is_set(values, key)]

    for key in required:
        mark = "OK " if is_set(values, key) else "MISSING"
        print(f"  [{mark}] {key}")

    if not missing:
        print()
        print(f"You're ready to start Task {args.task}.")
        return 0

    print()
    print("Set the following before starting this task:")
    for key in missing:
        print(f"\n  {key}\n    {FIX_HINTS.get(key, 'Add this key to your .env file.')}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
