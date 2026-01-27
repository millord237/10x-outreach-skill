---
name: seo
description: SEO optimization and keyword research with Exa AI
---

# /seo Command

Research keywords, analyze competitors, optimize content for search, and track rankings using Exa AI.

## Usage

```
/seo [action]
```

### Actions

- `/seo keywords <topic>` — Research keywords for a topic
- `/seo competitors <domain>` — Analyze competitor SEO
- `/seo audit <url>` — On-page SEO audit of a URL
- `/seo backlinks <domain>` — Backlink analysis and link-building opportunities
- `/seo optimize <content>` — Optimize content for target keywords
- `/seo report` — Generate a full SEO report

## Keyword Research Output

| Field | Description |
|-------|-------------|
| Keyword | The search term |
| Volume | Estimated monthly searches |
| Difficulty | Competition level (low/medium/high) |
| Intent | Informational, navigational, transactional, commercial |
| Related | Semantically related terms |

## Competitor Analysis

- Top ranking content for target keywords
- Content gaps and opportunities
- Domain authority estimates
- Traffic estimates
- Backlink profiles

## On-Page SEO Checklist

- Title tag optimization
- Meta description
- Heading structure (H1-H6)
- Content quality and length
- Image alt text
- Internal/external links
- Technical SEO (page speed, mobile, schema)

## Exa AI Integration

Uses Exa AI for:
- `web_search_exa` — SERP landscape analysis
- `company_research_exa` — Competitor domain analysis
- `deep_researcher_exa` — In-depth keyword research
- Websets for tracking ranking pages over time

## Examples

```
/seo keywords "AI sales automation"
/seo competitors "competitor.com"
/seo audit "https://mysite.com/blog/post"
/seo backlinks "mysite.com"
/seo optimize "paste your blog post content here"
```

## Skill Reference

This command uses the `seo-optimization` skill at `.claude/skills/seo-optimization/SKILL.md`.
