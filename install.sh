#!/usr/bin/env bash
# Installs the yt-transcript Claude skill for the current user.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skill/yt-transcript"
SKILL_DEST="$HOME/.claude/skills/yt-transcript"

if ! command -v python3 >/dev/null 2>&1; then
    echo "error: python3 is required but not found" >&2
    exit 1
fi

echo "Installing skill to $SKILL_DEST ..."
mkdir -p "$SKILL_DEST"
cp "$SKILL_SRC/SKILL.md" "$SKILL_SRC/fetch_transcript.py" "$SKILL_DEST/"

echo "Creating virtualenv and installing youtube-transcript-api ..."
python3 -m venv "$SKILL_DEST/.venv"
"$SKILL_DEST/.venv/bin/pip" install --quiet --upgrade pip
"$SKILL_DEST/.venv/bin/pip" install --quiet youtube-transcript-api

echo "Verifying installation ..."
"$SKILL_DEST/.venv/bin/python" -c "import youtube_transcript_api; print('youtube-transcript-api', youtube_transcript_api.__version__ if hasattr(youtube_transcript_api, '__version__') else 'OK')"

echo
echo "Done. Open Claude Code, paste a YouTube link, and ask for a summary —"
echo "the yt-transcript skill will trigger automatically."
