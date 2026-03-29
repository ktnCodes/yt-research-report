# YouTube Video → Research Report Generator

An MCP server + Claude Code skill that takes a YouTube video URL, extracts its transcript, and generates a polished Markdown research report for a Hugo blog.

## How It Works

Two components work together:

1. **MCP Server** (`src/server.py`) — A Python server exposing a `fetch_youtube_transcript` tool to Claude Code via the Model Context Protocol
2. **Custom Skill** (`/yt-report`) — A slash command that instructs Claude to fetch the transcript, analyze it, and generate a structured research report

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Register the MCP server

Add a `.mcp.json` file at your workspace root (e.g. `C:/Users/kevin/Portfolio/.mcp.json`):

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "python",
      "args": ["C:/Users/kevin/Portfolio/blog-tools/yt-research-report/src/server.py"]
    }
  }
}
```

### 3. Install the skill

The skill file lives in the repo at `skill/yt-report.md`. Copy it to your Claude skills directory:

```bash
cp skill/yt-report.md ~/.claude/skills/yt-report.md
```

### 4. Use it

Restart Claude Code, then run:

```
/yt-report https://www.youtube.com/watch?v=VIDEO_ID
```

A Markdown research report will be generated in your Hugo blog's `content/posts/` directory.

## Report Sections

- Embedded YouTube player (Hugo shortcode)
- Executive Summary
- Key Takeaways
- Detailed Analysis
- Timestamped Topic Outline (with clickable links)
- Sources & Further Reading

## Tech Stack

- Python 3.10+
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- Claude Code
