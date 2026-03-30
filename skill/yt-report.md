---
name: yt-report
description: Generate a research report from a YouTube video transcript
user_invocable: true
argument: url (required) — The YouTube video URL to generate a report from
---

# YouTube Research Report Generator

You are generating a structured research report from a YouTube video. Follow these steps exactly.

## Step 1: Fetch the Transcript

Call the `fetch_youtube_transcript` MCP tool with the provided URL: `$ARGUMENTS`

If the tool returns an error, inform the user and stop.

## Step 2: Fetch Video Metadata

Call the `fetch_video_metadata` MCP tool with the same URL: `$ARGUMENTS`

Use the returned `title` and `channel` fields for the report header. If the tool returns an error or empty fields, fall back to searching with the `WebSearch` tool using `youtube.com/watch?v=VIDEO_ID`.

## Step 3: Analyze the Transcript

Read through the entire formatted transcript and identify:
- The main thesis/argument of the video
- 5-7 key takeaways
- Major topic sections with their approximate timestamps
- Any sources, references, or further reading mentioned
- The overall narrative structure

## Step 4: Generate the Report

Create the report file at `C:\Users\kevin\Workspace\portfolio-site\ktncodes-v2\content\posts\` with a slugified filename based on the video title (e.g., `research-report-video-title.mdx`).

Use this exact format:

```markdown
---
title: "Research Report: [Video Title]"
date: [TODAY'S DATE in YYYY-MM-DD format]
tags: ["research", "youtube", "[topic-tag]"]
summary: "Research report based on '[Video Title]' by [Channel Name]."
showToc: true
---

## Video
<iframe width="100%" height="400" src="https://www.youtube.com/embed/VIDEO_ID" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
**Source:** [Video Title](VIDEO_URL) by [Channel Name]

---
## Executive Summary
[2-3 paragraphs synthesizing the video's main argument/thesis. Write in clear, professional prose. Do not simply repeat the transcript — distill and contextualize.]

---
## Key Takeaways
- [5-7 concise bullet points capturing the most important insights]

---
## Detailed Analysis
### [Topic Heading 1]
[In-depth analysis of this topic area. Add context where helpful. Group related transcript segments together into coherent narrative sections.]

### [Topic Heading 2]
[Continue with additional topic sections as needed. Typically 3-5 sections.]

---
## Timestamped Topic Outline
| Timestamp | Topic |
|-----------|-------|
| [0:00](VIDEO_URL&t=0s) | Introduction |
| [M:SS](VIDEO_URL&t=Xs) | [Topic description] |
[Continue for all major topic transitions identified in the transcript]

---
## Sources & Further Reading
- [Any papers, books, articles, tools, or resources mentioned in the video]
- [If none were explicitly mentioned, note: "No external sources were referenced in this video."]
```

## Important Guidelines

- **Video embed:** Use the `<iframe>` format shown above with `https://www.youtube.com/embed/VIDEO_ID`
- **File extension:** Always use `.mdx` (not `.md`)
- **Timestamp links:** Format as `[M:SS](VIDEO_URL&t=Xs)` where X is total seconds
- **Tone:** Professional and analytical, as if writing a research brief
- **Length:** The detailed analysis should be substantive — aim for 800-1500 words depending on video length
- **Do not hallucinate:** Only include information present in the transcript. If you add context, clearly frame it as such.
- **Tags:** Include "research", "youtube", and 1-2 topic-specific tags derived from the content
