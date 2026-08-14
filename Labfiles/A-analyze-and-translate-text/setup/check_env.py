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
import re
from pathlib import Path

# Escape sequences python-dotenv expands inside double-quoted values.
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'"}


def _parse_env_file(env_path):
    """Minimal stdlib .env reader, used when python-dotenv isn't installed.

    Kept at module level (rather than hidden inside the ImportError branch) so it
    can be imported and tested directly. Behaviour matches python-dotenv for the
    syntax a lab .env realistically uses: comments, blank lines, "export KEY=value",
    single/double-quoted values, inline comments, escapes inside double quotes,
    bare keys, and a UTF-8 BOM.

    A quoted value that doesn't close on its own line continues onto the following
    lines, exactly as python-dotenv does - so an unclosed quote really does consume
    the settings after it. If the quote never closes, or there's stray text after
    the closing quote, the entry is discarded (again matching python-dotenv).
    A missing or unreadable file yields {}.
    """
    values = {}
    try:
        # utf-8-sig so a BOM-prefixed .env parses cleanly too.
        with open(env_path, encoding="utf-8-sig") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return values

    index = 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if not line or line.startswith("#"):
            continue

        # "export KEY=value" - the separator may be a space or a tab. Guard the
        # length/character check so a key such as "exported" isn't truncated.
        if line.startswith("export") and len(line) > 6 and line[6] in " \t":
            line = line[6:].lstrip()

        key, separator, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        if not separator:
            # python-dotenv reports a key with no "=" as present but unset.
            values[key] = None
            continue

        value = value.strip()
        if value and value[0] in ("'", '"'):
            quote = value[0]
            body, closed, rest = _scan_quoted(value[1:], quote)
            if not closed:
                # Only continue onto the following lines if the quote actually
                # closes somewhere below. python-dotenv consumes those lines (so
                # an unclosed quote really does swallow the settings after it),
                # but when nothing ever closes it, it drops just this entry and
                # carries on - so look ahead before committing.
                lookahead = index
                while lookahead < len(lines):
                    _more, shut, _r = _scan_quoted(lines[lookahead], quote)
                    if shut:
                        break
                    lookahead += 1
                else:
                    continue  # never closes: discard this entry only
                while not closed and index < len(lines):
                    body.append("\n")
                    more, closed, rest = _scan_quoted(lines[index], quote)
                    body.extend(more)
                    index += 1
            # python-dotenv can't parse stray text after the closing quote and
            # drops the whole entry; a trailing comment is fine.
            leftover = rest.strip()
            if leftover and not leftover.startswith("#"):
                continue
            value = "".join(body)
            if quote == '"':
                value = re.sub(
                    r"\\(.)",
                    lambda match: _ESCAPES.get(match.group(1), "\\" + match.group(1)),
                    value,
                )
        else:
            # Unquoted: " #" starts an inline comment, but "bar#x" does not.
            comment = value.find(" #")
            if comment != -1:
                value = value[:comment].rstrip()
        values[key] = value

    return values


def _scan_quoted(text, quote):
    """Scan text for the closing quote.

    Returns (characters_before_it, closed, text_after_it). Inside double quotes a
    backslash escapes the next character, so an escaped quote doesn't end the value.
    """
    body = []
    index = 0
    while index < len(text):
        char = text[index]
        if quote == '"' and char == "\\" and index + 1 < len(text):
            body.append(text[index:index + 2])
            index += 2
            continue
        if char == quote:
            return body, True, text[index + 1:]
        body.append(char)
        index += 1
    return body, False, ""


def find_unclosed_quote(env_path):
    """Return (line_number, key) for a quoted value that doesn't close on its line.

    Such a value continues onto the following lines, so every setting after it is
    read as part of one value and the app never sees them. Returns (None, None)
    when there's nothing wrong.
    """
    try:
        with open(env_path, encoding="utf-8-sig") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return None, None

    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export") and len(line) > 6 and line[6] in " \t":
            line = line[6:].lstrip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        value = value.strip()
        if value and value[0] in ("'", '"'):
            _body, closed, _rest = _scan_quoted(value[1:], value[0])
            if not closed:
                return number, key.strip()
    return None, None


try:
    from dotenv import dotenv_values
except ModuleNotFoundError:
    # python-dotenv is installed into the lab's virtual environment, but this
    # preflight check is meant to run BEFORE you install anything - and from a
    # terminal where labenv may not be activated. Fall back to the stdlib parser.
    dotenv_values = _parse_env_file

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


BOM_HINT = (
    "\n  .env encoding\n"
    "    Your .env was saved as 'UTF-8 with BOM' (Notepad does this by default).\n"
    "    The BOM becomes part of the first setting's name, so the app reads that\n"
    "    setting as empty even though the file looks correct.\n"
    "    Re-save it as plain UTF-8: in VS Code, click the encoding in the status\n"
    "    bar, choose 'Save with Encoding', then 'UTF-8' (not 'UTF-8 with BOM')."
)


QUOTE_HINT = (
    "\n  .env line {line} ({key})\n"
    "    This value opens a quote that is never closed on the same line, so it\n"
    "    keeps reading into the lines below it. Every setting after it becomes\n"
    "    part of one long value and the app never sees them.\n"
    "    Close the quote on line {line} (or remove both quotes - the lab values\n"
    "    don't need them)."
)


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


def has_utf8_bom(env_path):
    """True if the .env starts with a UTF-8 BOM.

    This matters because it genuinely breaks the lab apps, not just this check:
    load_dotenv() keeps the BOM on the first setting's name, so the app's
    os.getenv("FOUNDRY_ENDPOINT") returns None even though the file looks right.
    """
    try:
        with open(env_path, "rb") as handle:
            return handle.read(3) == b"\xef\xbb\xbf"
    except OSError:
        return False


def load_values(env_path):
    """Merge real environment variables over .env file values (env wins)."""
    values = {}
    if env_path.exists():
        for key, value in dotenv_values(env_path).items():
            if value is None:
                continue
            # Normalize a BOM off the first key so the per-key listing reflects
            # what you actually typed. The BOM is still reported as a problem by
            # has_utf8_bom() - it is fatal for the app, so it must not pass
            # silently just because the value is present.
            values[key.lstrip("\ufeff").strip()] = value
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
    bom = env_path.exists() and has_utf8_bom(env_path)
    quote_line, quote_key = (None, None)
    if env_path.exists():
        quote_line, quote_key = find_unclosed_quote(env_path)

    for key in required:
        mark = "OK " if is_set(values, key) else "MISSING"
        print(f"  [{mark}] {key}")

    if bom:
        print("  [PROBLEM] .env starts with a UTF-8 BOM")
    if quote_line:
        print(f"  [NOTE] .env line {quote_line}: unterminated quote")

    if not missing and not bom:
        if quote_line:
            print()
            print(QUOTE_HINT.format(line=quote_line, key=quote_key))
            print("  (Nothing this task needs is affected, but it's worth fixing.)")
        print()
        print(f"You're ready to start Task {args.task}.")
        return 0

    print()
    if bom:
        print("Fix the following before starting this task:")
        print(BOM_HINT)
    if quote_line:
        print(QUOTE_HINT.format(line=quote_line, key=quote_key))
    if missing:
        print("Set the following before starting this task:")
        for key in missing:
            print(f"\n  {key}\n    {FIX_HINTS.get(key, 'Add this key to your .env file.')}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
