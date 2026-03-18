# YouTube Video → Research Report Generator — Plan

## Context

A portfolio project to learn AI usage. Takes a YouTube video URL, extracts its transcript, and generates a polished Markdown research report. Starting with the free approach (MCP Server + Claude Code), with plans to expand into a standalone application later.

Reports target the Hugo blog at `C:\Workspace\Projects\ktncodes.github.io`, but the tool itself lives in its own project folder.

## Approach: MCP Server + Custom Skill (Free)

1. **MCP Server** — Python server exposing `fetch_youtube_transcript` tool
2. **Custom Skill** — `/yt-report` slash command for one-command workflow

**Cost: $0 extra** — runs entirely within existing Claude Code session.

## Report Format

See `README.md` for section overview. Full template is embedded in the skill definition at `~/.claude/skills/yt-report.md`.

## Future Expansion (Phase 2)

- Standalone Python CLI with `anthropic` SDK
- GitHub Actions workflow for remote triggering
- Additional MCP tools (video metadata, channel info, thumbnail fetching)
