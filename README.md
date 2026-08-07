# YouTube Transcripts for Claude

A [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) that automatically fetches YouTube video transcripts. Paste a YouTube link into Claude Code (or claude.ai) and ask for a summary, key points, or anything else — Claude pulls the transcript locally via [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api) and works from the actual video content instead of guessing.

```
You:    Summarize https://www.youtube.com/watch?v=dQw4w9WgXcQ
Claude: [fetches the transcript automatically, then summarizes it]
```

## Features

- **Automatic triggering** — no command to remember. Any YouTube URL (watch, `youtu.be`, Shorts, embed, live) or bare video ID activates the skill.
- **Three output formats** — plain text for summaries, `[MM:SS]` timestamped lines for referencing moments, JSON for programmatic use.
- **Language support** — request a specific language (`--lang hi`), with automatic fallback to English or any available transcript.
- **No API key required** — uses YouTube's public transcript endpoints via `youtube-transcript-api`.
- **Works in the cloud too** — the skill is self-contained, so it can be uploaded to claude.ai and run in the cloud sandbox.

## Requirements

- Python 3.8+
- [Claude Code](https://claude.com/claude-code) (CLI or desktop app)

## Install (Claude Code)

```bash
git clone https://github.com/prat3ik/youtube-transcripts-for-claude.git
cd youtube-transcripts-for-claude
./install.sh
```

The install script:

1. Copies the skill to `~/.claude/skills/yt-transcript/`
2. Creates a virtualenv inside the skill folder
3. Installs `youtube-transcript-api` into it

That's it. Open Claude Code anywhere, paste a YouTube link, and ask away.

## Install (claude.ai)

Skills on claude.ai run in a cloud sandbox, so the skill installs its own dependency there. To upload:

```bash
cd skill && zip -r yt-transcript-skill.zip yt-transcript
```

Then in claude.ai: **Settings → Capabilities → Skills → Upload skill** and select the zip.

> **Note:** YouTube sometimes rate-limits requests from datacenter IPs, so the cloud version may occasionally be blocked where the local one succeeds.

## Usage examples

Once installed, just talk to Claude naturally:

- `Summarize https://youtu.be/VIDEO_ID`
- `What are the key takeaways from this talk? https://www.youtube.com/watch?v=VIDEO_ID`
- `Get the transcript of this video with timestamps: <url>`
- `Translate the main points of <url> into Hindi`

You can also run the fetcher directly:

```bash
~/.claude/skills/yt-transcript/.venv/bin/python \
  ~/.claude/skills/yt-transcript/fetch_transcript.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format timestamped
```

### CLI options

| Option | Values | Description |
|---|---|---|
| `--format` | `text` (default), `timestamped`, `json` | Output format |
| `--lang` | Any language code, e.g. `en`, `hi`, `es` | Preferred transcript language; falls back automatically |

## How it works

```
YouTube URL ──> SKILL.md (auto-triggers on YouTube links)
                   │
                   ▼
            fetch_transcript.py ──> youtube-transcript-api ──> YouTube
                   │
                   ▼
            transcript (text / timestamped / JSON) ──> Claude processes it
```

The skill's `SKILL.md` description tells Claude when to activate (any message containing a YouTube link that needs transcription/summarization). Claude then runs the bundled `fetch_transcript.py`, which extracts the video ID, fetches the best-matching transcript, and prints it for Claude to work with.

## Troubleshooting

| Problem | Fix |
|---|---|
| `transcripts are disabled` | The channel turned off captions — no transcript exists for that video. |
| `no transcript found` | The video has no captions in any language. |
| `RequestBlocked` / network errors | YouTube is rate-limiting your IP (common on cloud/VPN). Wait and retry. |
| Skill doesn't trigger | Check the skill is at `~/.claude/skills/yt-transcript/SKILL.md`, then restart Claude Code. |
| Import errors | Re-run `./install.sh` to rebuild the virtualenv. |

## Credits

- Transcript fetching by [jdepoix/youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) (MIT).

## License

[MIT](LICENSE)
