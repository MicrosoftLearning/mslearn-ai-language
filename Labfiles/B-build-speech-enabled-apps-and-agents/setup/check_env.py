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
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'"}


def _parse_env_file(env_path):
    """Minimal stdlib .env reader, used when python-dotenv isn't installed.

    Kept at module level (rather than hidden inside the ImportError branch) so it
    can be imported and tested directly. Behaviour matches python-dotenv for the
    syntax a lab .env realistically uses: comments, blank lines, "export KEY=value",
    single/double-quoted values, inline comments, escapes inside double quotes,
    bare keys, and a UTF-8 BOM. An unterminated quoted value is discarded, and a
    missing or unreadable file yields {}.
    """
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
            # Quoted: scan to the matching close quote so anything after it (such
            # as an inline comment) is ignored, and a "#" inside the quotes is
            # kept. Inside double quotes a backslash escapes the next character.
            quote = value[0]
            body = []
            index = 1
            closed = False
            while index < len(value):
                char = value[index]
                if quote == '"' and char == "\\" and index + 1 < len(value):
                    body.append(value[index:index + 2])
                    index += 2
                    continue
                if char == quote:
                    closed = True
                    break
                body.append(char)
                index += 1
            if not closed:
                # python-dotenv discards an entry whose quote is never closed.
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
        for key, value in dotenv_values(env_path).items():
            if value is None:
                continue
            # A .env saved by Windows Notepad starts with a UTF-8 BOM, and
            # python-dotenv keeps it on the first key ("\ufeffSPEECH_ENDPOINT"),
            # which would report a correctly set key as missing. Strip it so both
            # this and the stdlib fallback agree.
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
        help="Which task you're about to start (1-5).",
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
