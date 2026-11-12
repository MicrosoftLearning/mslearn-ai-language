"""
Preflight check for the Alpine Ski House guest services voice lab (Lab B).

Each task in this lab can be completed on its own. Before you start a task,
run this script to confirm your .env file has everything that task needs.

Run it from the starter code folder - Labfiles/B-build-speech-enabled-apps-and-agents/Python -
which is the folder you opened in VS Code and where your terminal is already open:

    python ../setup/check_env.py --task 2

(If you run it from the lab root instead, drop the '../' and use
'python setup/check_env.py --task 2'. Note that this script is NOT reachable from
Solution/Python, because there is no Solution/setup folder.)

It never changes anything - it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (code)   SPEECH_ENDPOINT
    Task 2  (code)   TTS_MODEL_ENDPOINT, TTS_MODEL_NAME, STT_MODEL_ENDPOINT, STT_MODEL_NAME
    Task 3  (code)   SPEECH_ENDPOINT
    Task 4  (code)   PROJECT_ENDPOINT, AGENT_NAME
    Task 5  (code)   VOICELIVE_ENDPOINT, VOICELIVE_PROJECT_NAME, VOICELIVE_AGENT_NAME
"""

import argparse
import os
import re
from pathlib import Path

# Escape sequences python-dotenv expands inside double-quoted values.
_ESCAPES = {
    "n": "\n", "t": "\t", "r": "\r", "a": "\a", "b": "\b", "f": "\f", "v": "\v",
    "\\": "\\", '"': '"', "'": "'",
}
# Single-quoted values only unescape the quote itself and a literal backslash;
# "\n" and friends stay literal in single quotes.
_ESCAPES_SINGLE = {"\\": "\\", "'": "'"}


def _parse_env_file(env_path):
    """Minimal stdlib .env reader, used when python-dotenv isn't installed.

    Kept at module level (rather than hidden inside the ImportError branch) so it
    can be imported and tested directly. Behaviour matches python-dotenv for the
    syntax a lab .env realistically uses: comments, blank lines, "export KEY=value",
    single/double-quoted values, inline comments, escapes inside double quotes,
    A quoted value that doesn't close on its own line continues onto the following
    lines, exactly as python-dotenv does - so an unclosed quote really does consume
    the settings after it. If the quote never closes anywhere below, only that entry
    is dropped. A missing or unreadable file yields {}.

    INTENTIONAL DIVERGENCE - do not "fix" this to match python-dotenv:
    reading with utf-8-sig strips a UTF-8 BOM, whereas python-dotenv keeps it and
    returns a first key of "\ufeffSPEECH_ENDPOINT". Matching dotenv here would
    make this parser more faithful and the check less useful: the BOM is reported
    separately by has_utf8_bom(), which is what blocks, and that detector reads raw
    bytes so it stays correct however this parser changes. A parity test cannot
    catch a regression here, because dotenv's own behaviour is the broken one.
    """
    values = {}
    try:
        # utf-8-sig: see the INTENTIONAL DIVERGENCE note above.
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
                #
                # It looks ahead escape-aware first; only if that finds nothing
                # does it fall back to treating a backslash-escaped quote as a
                # real one. Both passes are needed: escape-aware alone misses a
                # line whose only quote is \" (dotenv still closes there), and
                # raw alone closes too early when a genuine quote follows later.
                escape_aware = True
                closer = _find_closing_line(lines, index, quote, True)
                if closer is None:
                    escape_aware = False
                    closer = _find_closing_line(lines, index, quote, False)
                if closer is None:
                    continue  # never closes: discard this entry only
                while not closed and index < len(lines):
                    body.append("\n")
                    more, closed, rest = _scan_quoted(lines[index], quote, escape_aware)
                    body.extend(more)
                    index += 1
            # python-dotenv can't parse stray text after the closing quote and
            # drops the whole entry; a trailing comment is fine.
            leftover = rest.strip()
            if leftover and not leftover.startswith("#"):
                continue
            value = "".join(body)
            escapes = _ESCAPES if quote == '"' else _ESCAPES_SINGLE
            value = re.sub(
                r"\\(.)",
                lambda match: escapes.get(match.group(1), "\\" + match.group(1)),
                value,
            )
        else:
            # Unquoted: " #" starts an inline comment, but "bar#x" does not.
            comment = value.find(" #")
            if comment != -1:
                value = value[:comment].rstrip()
        values[key] = value

    return values


def _scan_quoted(text, quote, escape_aware=True):
    """Scan text for the closing quote.

    Returns (characters_before_it, closed, text_after_it). A backslash escapes the
    next character for BOTH quote styles - python-dotenv honours \\' inside single
    quotes as well as \\" inside double quotes - except when recovering from a
    quote that never closes, where it stops honouring them (escape_aware=False).
    """
    body = []
    index = 0
    while index < len(text):
        char = text[index]
        if escape_aware and char == "\\" and index + 1 < len(text):
            body.append(text[index:index + 2])
            index += 2
            continue
        if char == quote:
            return body, True, text[index + 1:]
        body.append(char)
        index += 1
    return body, False, ""


def _find_closing_line(lines, start, quote, escape_aware):
    """Index of the first line at or after start that closes quote, else None."""
    for offset in range(start, len(lines)):
        _body, closed, _rest = _scan_quoted(lines[offset], quote, escape_aware)
        if closed:
            return offset
    return None


def find_placeholders():
    """PLACEHOLDERS plus any placeholder-shaped value in the shipped .env.example.

    Keeping the two in sync by hand rots: edit .env.example, forget the list, and
    an unedited .env is reported ready. Reading the example at runtime removes the
    coupling.

    Only placeholder-SHAPED values are absorbed. Some example values are
    deliberately real - the agent names a learner is told to create, the model
    deployment names - and treating those as placeholders would reject a correctly
    filled .env.
    """
    placeholders = set(PLACEHOLDERS)
    example = Path(__file__).resolve().parent.parent / "Python" / ".env.example"
    for value in _parse_env_file(example).values():
        if not value:
            continue
        value = value.strip()
        if value.startswith("your_") or value.startswith("your-") or (
                value.startswith("<") and value.endswith(">")):
            placeholders.add(value)
    return placeholders


def key_line_numbers(env_path):
    """Map each KEY to the line number where it's assigned (last wins).

    Used to decide whether a setting appears before or after an unclosed quote.
    Scans the raw text, so it doesn't depend on how the value parses.
    """
    numbers = {}
    try:
        with open(env_path, encoding="utf-8-sig") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return numbers

    for number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export") and len(line) > 6 and line[6] in " \t":
            line = line[6:].lstrip()
        key, separator, _value = line.partition("=")
        if separator:
            numbers[key.strip().lstrip("\ufeff")] = number
    return numbers


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
    1: ["SPEECH_ENDPOINT"],
    2: ["TTS_MODEL_ENDPOINT", "TTS_MODEL_NAME", "STT_MODEL_ENDPOINT", "STT_MODEL_NAME"],
    3: ["SPEECH_ENDPOINT"],
    4: ["PROJECT_ENDPOINT", "AGENT_NAME"],
    5: ["VOICELIVE_ENDPOINT", "VOICELIVE_PROJECT_NAME", "VOICELIVE_AGENT_NAME"],
}

ALL_KEYS = (
    "SPEECH_ENDPOINT",
    "TTS_MODEL_ENDPOINT",
    "TTS_MODEL_NAME",
    "STT_MODEL_ENDPOINT",
    "STT_MODEL_NAME",
    "PROJECT_ENDPOINT",
    "AGENT_NAME",
    "VOICELIVE_ENDPOINT",
    "VOICELIVE_PROJECT_NAME",
    "VOICELIVE_AGENT_NAME",
)

# Placeholder text shipped in .env.example - present but not yet filled in.
PLACEHOLDERS = {
    "",
    "your_speech_endpoint",
    "your_tts_model_endpoint",
    "your_stt_model_endpoint",
    "your_project_endpoint",
    "your_voicelive_endpoint",
    "your_project_name",
    "<your_speech_endpoint>",
    "<your_project_endpoint>",
    "<your_voicelive_endpoint>",
}

# How to fix each key, shown only when it's missing.
FIX_HINTS = {
    "SPEECH_ENDPOINT": (
        "The Azure Speech SDK uses the Azure AI services form of your Foundry resource "
        "endpoint. It should look like "
        "https://your-resource.cognitiveservices.azure.com/"
    ),
    "TTS_MODEL_ENDPOINT": (
        "Set this to the Target URI of your text-to-speech model deployment. Copy it "
        "from the model details page in the Microsoft Foundry portal."
    ),
    "TTS_MODEL_NAME": (
        "Set this to the deployment name of your text-to-speech model "
        "(for example, gpt-4o-mini-tts)."
    ),
    "STT_MODEL_ENDPOINT": (
        "Set this to the Target URI of your speech-to-text model deployment. Copy it "
        "from the model details page in the Microsoft Foundry portal."
    ),
    "STT_MODEL_NAME": (
        "Set this to the deployment name of your speech-to-text model "
        "(for example, gpt-4o-mini-transcribe)."
    ),
    "PROJECT_ENDPOINT": (
        "Task 4 uses the full project endpoint, including the "
        "'/api/projects/{project_name}' suffix. Copy it from the project overview "
        "page in the Microsoft Foundry portal."
    ),
    "AGENT_NAME": (
        "Task 4 needs the agent you create in the Foundry portal. Set "
        "AGENT_NAME=slope-report-agent (the name is case-sensitive)."
    ),
    "VOICELIVE_ENDPOINT": (
        "Voice Live uses the project endpoint with the "
        "'/api/projects/{project_name}' suffix removed, so it ends at the .com "
        "domain: https://your-resource.services.ai.azure.com/"
    ),
    "VOICELIVE_PROJECT_NAME": (
        "Set this to the name of your Foundry project (not the resource name)."
    ),
    "VOICELIVE_AGENT_NAME": (
        "Task 5 needs the voice agent you create in the Foundry portal. Set "
        "VOICELIVE_AGENT_NAME=concierge-agent (the name is case-sensitive)."
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
    os.getenv("SPEECH_ENDPOINT") returns None even though the file looks right.
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


def is_set(values, key, placeholders=None):
    """A key counts as set if it's present, not a placeholder, and plausible.

    Endpoint settings are URLs, so anything that isn't one is still template text
    however it's worded - that catches a renamed placeholder the list hasn't
    learned yet, and a learner who pasted the wrong thing.
    """
    value = (values.get(key) or "").strip()
    known = PLACEHOLDERS if placeholders is None else placeholders
    if not value or value in known:
        return False
    if key.endswith("_ENDPOINT") and not value.lower().startswith("http"):
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Check that your .env has what a given lab task needs."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(TASK_REQUIREMENTS),
        required=True,
        help="Which task you're about to start (1-5).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    placeholders = find_placeholders()
    required = TASK_REQUIREMENTS[args.task]

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    missing = [key for key in required if not is_set(values, key, placeholders)]
    bom = env_path.exists() and has_utf8_bom(env_path)
    quote_line, quote_key = (None, None)
    if env_path.exists():
        quote_line, quote_key = find_unclosed_quote(env_path)

    # Anything written at or below an unclosed quote may have been swallowed into
    # that value, so its apparent presence here can't be trusted - the app may not
    # see it. Treat those as unverified rather than reporting them as ready.
    suspect = []
    if quote_line:
        line_of = key_line_numbers(env_path)
        suspect = [
            key for key in required
            if key not in missing and line_of.get(key, 0) >= quote_line
        ]

    for key in required:
        if key in suspect:
            mark = "UNSURE"
        elif is_set(values, key, placeholders):
            mark = "OK "
        else:
            mark = "MISSING"
        print(f"  [{mark}] {key}")

    if bom:
        print("  [PROBLEM] .env starts with a UTF-8 BOM")
    if quote_line:
        print(f"  [NOTE] .env line {quote_line}: unterminated quote")

    if not missing and not bom and not suspect:
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
