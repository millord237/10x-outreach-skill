---
name: content
description: Content marketing and creation with Exa AI research
---

# /content Command

Create blog posts, social media content, content calendars, and research trending topics using Exa AI.

## Usage

```
/content [action]
```

### Actions

- `/content research <topic>` — Research a topic using Exa AI semantic search
- `/content blog <topic>` — Generate a blog post with SEO optimization
- `/content linkedin <topic>` — Create a LinkedIn post
- `/content twitter <topic>` — Create a Twitter thread
- `/content instagram <topic>` — Create an Instagram caption
- `/content calendar` — Plan a content calendar for the week/month
- `/content trends <industry>` — Discover trending topics in an industry

## Content Types

| Type | Format | Platform |
|------|--------|----------|
| Blog post | Long-form with headings, intro, body, conclusion | Website |
| LinkedIn post | Hook + value points + CTA + hashtags | LinkedIn |
| Twitter thread | 6-part thread with hook and CTA | Twitter/X |
| Instagram caption | Hook + content + CTA + 30 hashtags | Instagram |

## Exa AI Integration

Uses Exa AI for:
- `web_search_exa` — Semantic topic research
- `company_research_exa` — Competitor content analysis
- `deep_researcher_exa` — In-depth trend discovery

## Examples

```
/content research "AI in logistics 2026"
/content blog "How to use AI for sales prospecting"
/content linkedin "remote work productivity tips"
/content twitter "startup fundraising lessons"
/content calendar --weeks 4 --platforms linkedin,twitter
/content trends "SaaS B2B"
```

## Skill Reference

This command uses the `content-marketing` skill at `.claude/skills/content-marketing/SKILL.md`.
