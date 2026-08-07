---
name: yt-transcript
description: Fetch the transcript of a YouTube video whenever the user provides a YouTube URL (youtube.com/watch, youtu.be, Shorts, embed, or live links) or a video ID and wants the video transcribed, summarized, analyzed, or its content processed. Use this instead of trying to fetch the page or watch the video.
---

# YouTube Transcript Fetcher

Fetch a YouTube video's transcript using `youtube-transcript-api`. The fetcher script (`fetch_transcript.py`) lives in this skill's folder, next to this SKILL.md.

## How to fetch a transcript

**If the installed venv exists** (created by the project's `install.sh`), prefer it:

```bash
~/.claude/skills/yt-transcript/.venv/bin/python ~/.claude/skills/yt-transcript/fetch_transcript.py "<YOUTUBE_URL_OR_ID>" --format timestamped
```

**Otherwise** (cloud sandbox, claude.ai, or venv missing), install the library and run the bundled script with the system Python:

```bash
pip install youtube-transcript-api
python3 <path-to-this-skill>/fetch_transcript.py "<YOUTUBE_URL_OR_ID>" --format timestamped
```

## Options

- Accepts full URLs (`youtube.com/watch?v=...`, `youtu.be/...`, Shorts, embed, live) or a bare 11-character video ID.
- `--format text` — plain text, one line (best for summarization).
- `--format timestamped` — `[MM:SS] text` lines (best when the user wants to reference moments in the video).
- `--format json` — structured snippets with `start`/`duration` (best for programmatic processing).
- `--lang <code>` — preferred language (e.g. `en`, `hi`). Falls back to English, then to any available transcript.

## Workflow

1. Extract the YouTube URL or video ID from the user's message.
2. For long videos, write output to a temp file and read it in chunks rather than dumping it all to the terminal:
   ```bash
   ... fetch_transcript.py "<URL>" --format timestamped > /tmp/transcript.txt
   ```
3. Process the transcript per the user's request (summarize, extract key points, answer questions, translate, etc.). If they gave no specific instruction, provide a concise summary with key takeaways.

## Errors

- `transcripts are disabled` — the channel turned off captions; tell the user no transcript is available.
- `no transcript found` — the script already falls back to any available language; if it still fails, the video has no captions.
- Network/IP block errors (e.g. `RequestBlocked`) — YouTube may be rate-limiting (common from datacenter IPs); wait and retry once, then inform the user.
- Missing venv or import errors — reinstall with `pip install youtube-transcript-api`, or re-run the project's `install.sh`.
