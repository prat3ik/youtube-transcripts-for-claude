#!/usr/bin/env python3
"""Fetch a YouTube transcript given a URL or video ID.

Usage:
    fetch_transcript.py <url-or-video-id> [--lang en] [--format text|json|timestamped]

Outputs the transcript to stdout so it can be piped or read directly.
"""

import argparse
import json
import re
import sys
import warnings

warnings.filterwarnings("ignore")

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

VIDEO_ID_PATTERNS = [
    r"(?:youtube\.com/watch\?(?:.*&)?v=)([\w-]{11})",
    r"(?:youtu\.be/)([\w-]{11})",
    r"(?:youtube\.com/shorts/)([\w-]{11})",
    r"(?:youtube\.com/embed/)([\w-]{11})",
    r"(?:youtube\.com/live/)([\w-]{11})",
]


def extract_video_id(url_or_id: str) -> str:
    if re.fullmatch(r"[\w-]{11}", url_or_id):
        return url_or_id
    for pattern in VIDEO_ID_PATTERNS:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    sys.exit(f"error: could not extract a video ID from: {url_or_id}")


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="YouTube URL or 11-character video ID")
    parser.add_argument(
        "--lang",
        default=None,
        help="Preferred language code (e.g. en, hi). Falls back to any available.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "timestamped"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.video)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)
        languages = [args.lang] if args.lang else ["en"]
        try:
            transcript = transcript_list.find_transcript(languages)
        except NoTranscriptFound:
            # Fall back to the first available transcript in any language
            transcript = next(iter(transcript_list))
        fetched = transcript.fetch()
    except TranscriptsDisabled:
        sys.exit(f"error: transcripts are disabled for video {video_id}")
    except VideoUnavailable:
        sys.exit(f"error: video {video_id} is unavailable")
    except NoTranscriptFound:
        sys.exit(f"error: no transcript found for video {video_id}")

    snippets = fetched.snippets
    if args.format == "json":
        print(
            json.dumps(
                {
                    "video_id": video_id,
                    "language": fetched.language,
                    "language_code": fetched.language_code,
                    "is_generated": fetched.is_generated,
                    "snippets": [
                        {"text": s.text, "start": s.start, "duration": s.duration}
                        for s in snippets
                    ],
                },
                ensure_ascii=False,
            )
        )
    elif args.format == "timestamped":
        print(f"# Video: {video_id} | Language: {fetched.language}")
        for s in snippets:
            print(f"[{format_timestamp(s.start)}] {s.text.replace(chr(10), ' ')}")
    else:
        print(" ".join(s.text.replace("\n", " ") for s in snippets))


if __name__ == "__main__":
    main()
