"""MCP server that exposes YouTube transcript and metadata fetching tools."""

import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi

mcp = FastMCP("youtube-transcript")
ytt_api = YouTubeTranscriptApi()

CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    parsed = urlparse(url)

    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            qs = parse_qs(parsed.query)
            if "v" in qs:
                return qs["v"][0]
        elif parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
        elif parsed.path.startswith("/v/"):
            return parsed.path.split("/")[2]
    elif parsed.hostname in ("youtu.be",):
        return parsed.path.lstrip("/")

    # Last resort: try regex
    match = re.search(r"(?:v=|/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)

    raise ValueError(f"Could not extract video ID from URL: {url}")


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS or H:MM:SS format."""
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


@mcp.tool()
def fetch_youtube_transcript(url: str) -> str:
    """Fetch the transcript of a YouTube video.

    Takes a YouTube URL and returns the video ID, raw transcript segments,
    and a formatted transcript with timestamps for easy reference.
    Falls back to auto-generated captions if English is unavailable.

    Args:
        url: A YouTube video URL (youtube.com/watch?v=, youtu.be/, etc.)
    """
    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    # Check cache
    cache_file = CACHE_DIR / f"{video_id}.json"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    try:
        transcript_list = ytt_api.list(video_id)
        try:
            transcript = transcript_list.find_transcript(["en"])
        except Exception:
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )
        segments = transcript.fetch()
        language_code = transcript.language_code
        is_generated = transcript.is_generated
    except Exception as e:
        error_msg = str(e)
        if "disabled" in error_msg.lower():
            return json.dumps({
                "error": f"Transcripts are disabled for video {video_id}."
            })
        if "private" in error_msg.lower() or "unavailable" in error_msg.lower():
            return json.dumps({
                "error": f"Video {video_id} is private or unavailable."
            })
        return json.dumps({"error": f"Could not fetch transcript: {error_msg}"})

    formatted_lines = []
    for seg in segments:
        ts = format_timestamp(seg.start)
        formatted_lines.append(f"[{ts}] {seg.text}")

    raw_segments = [
        {"text": seg.text, "start": seg.start, "duration": seg.duration}
        for seg in segments
    ]

    result = {
        "video_id": video_id,
        "url": url,
        "language_code": language_code,
        "is_generated": is_generated,
        "transcript": raw_segments,
        "formatted_transcript": "\n".join(formatted_lines),
    }

    result_json = json.dumps(result)
    cache_file.write_text(result_json, encoding="utf-8")

    return result_json


@mcp.tool()
def fetch_video_metadata(url: str) -> str:
    """Fetch metadata for a YouTube video (title, channel, description).

    Uses the YouTube page's Open Graph meta tags — no API key required.

    Args:
        url: A YouTube video URL (youtube.com/watch?v=, youtu.be/, etc.)
    """
    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    try:
        req = Request(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        html = urlopen(req, timeout=10).read().decode("utf-8", errors="replace")
    except Exception as e:
        return json.dumps({"error": f"Could not fetch video page: {e}"})

    def extract_meta(pattern: str) -> str:
        match = re.search(pattern, html)
        return match.group(1) if match else ""

    title = extract_meta(r'<meta property="og:title" content="([^"]+)"')
    description = extract_meta(r'<meta property="og:description" content="([^"]+)"')
    channel = extract_meta(r'"author":"([^"]+)"')
    if not channel:
        channel = extract_meta(r'<link itemprop="name" content="([^"]+)"')

    result = {
        "video_id": video_id,
        "url": url,
        "title": title,
        "channel": channel,
        "description": description,
    }
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()
