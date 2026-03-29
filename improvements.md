# yt-research-report — Known Issues & Improvements

Tracked against the current state of the project as of 2026-03-29.

---

## Bugs / Broken State

**1. Hardcoded paths in README are wrong**
The setup instructions tell users to register the MCP server at `C:/Workspace/Projects/yt-research-report/src/server.py`. The actual project lives at `C:/Users/kevin/Portfolio/blog-tools/yt-research-report/src/server.py`. Anyone following the README will register a non-existent path and the MCP server will silently fail to start.

**2. Skill file not included in the repo**
`README.md` and `PLAN.md` both reference a `/yt-report` skill at `~/.claude/skills/yt-report.md`, but this file is not in the repository. The skill is the main user-facing interface — without it, the tool has no one-command workflow. The repo is incomplete as shipped.

**3. English-only transcript fetching**
`server.py:64` calls `ytt_api.fetch(video_id, languages=["en"])`. Any video without English captions will fail. There is no fallback to auto-generated captions or other languages.

---

## Missing Features (Phase 1 gaps)

**4. No video metadata**
The MCP server only fetches transcripts. It returns no title, channel name, description, publish date, duration, or thumbnail URL. The report generator has to guess or leave these blank. `PLAN.md` lists metadata fetching as Phase 2, but it's needed for even a basic report header.

**5. No output directory**
There is no `output/` folder in the project. The README and CONTEXT.md both reference writing reports to `blog-tools/output/`, but the directory doesn't exist and is not created by any script or setup step.

**6. No transcript caching**
Every invocation re-fetches the full transcript over the network. For the same video, this is wasteful and adds latency. There is no local cache, so re-running the skill on the same URL is slower than it needs to be.

---

## Quality / Maintainability

**7. requirements.txt has no version pins**
`requirements.txt` contains only `youtube-transcript-api` and `mcp` with no version constraints. Both libraries have had breaking API changes in recent major versions. Without pins, a fresh install may break silently depending on the environment.

**8. No test coverage**
`extract_video_id` handles six distinct URL formats and has a regex fallback — this is the most likely function to break on edge cases. There are no unit tests for it or for `format_timestamp`.

**9. Phase 2 not started**
`PLAN.md` lists a standalone Python CLI, GitHub Actions remote trigger, and additional MCP tools (metadata, thumbnails) as Phase 2. None of these have been started. The gap between Phase 1 and the stated end goal is large and untracked.
