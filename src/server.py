"""MCP server that exposes a YouTube transcript fetching tool."""

import json
import re
from urllib.parse import parse_qs, urlparse

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi

mcp = FastMCP("youtube-transcript")


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


def seconds_to_url_param(seconds: float) -> int:
    """Convert seconds to integer for YouTube &t= parameter."""
    return int(seconds)


@mcp.tool()
def fetch_youtube_transcript(url: str) -> str:
    """Fetch the transcript of a YouTube video.

    Takes a YouTube URL and returns the video ID, raw transcript segments,
    and a formatted transcript with timestamps for easy reference.

    Args:
        url: A YouTube video URL (youtube.com/watch?v=, youtu.be/, etc.)
    """
    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
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

    # Prefer manually created transcripts, fall back to auto-generated
    try:
        transcript = transcript_list.find_manually_created_transcript(["en"])
    except Exception:
        try:
            transcript = transcript_list.find_generated_transcript(["en"])
        except Exception:
            return json.dumps({
                "error": "No English transcript available for this video."
            })

    segments = transcript.fetch()

    # Build formatted transcript with timestamp markers
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
        "transcript": raw_segments,
        "formatted_transcript": "\n".join(formatted_lines),
    }

    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()
