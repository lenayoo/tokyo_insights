# Tokyo Insight - AGENTS.md

## Project Overview

Tokyo Insight is a YouTube Shorts content system focused on:

* Japanese culture
* Tokyo lifestyle
* Japanese work culture
* Technology trends in Japan
* AI in Japan
* Consumer behavior
* Daily life observations
* News interpretation from a Tokyo resident perspective

The channel tone should feel:

* Calm
* Thoughtful
* Slightly cinematic
* Human
* Observational
* Never robotic or generic

The perspective is:
"A Korean developer living in Tokyo observing Japanese society from the inside."

---

# Goals

The system should help generate:

* Daily Shorts ideas
* Scripts
* Hooks
* Captions
* B-roll suggestions
* HTML preview pages
* Topic archives

The workflow should optimize for:

* Speed
* Consistency
* Repeatable production
* Shorts-friendly pacing
* High curiosity hooks

The target production speed is:
3-5 Shorts per day within 2 hours.

---

# Project Structure

```txt
tokyo-insight/
  AGENTS.md
  README.md
  index.html

  data/
    2026-05-29.json

  posts/
    2026-05-29.html

  scripts/
    generate_daily_topics.py

  assets/
    logo.png
```

---

# Folder Rules

## /data

Store structured JSON topic data.

Example:

```json
{
  "date": "2026-05-29",
  "topics": [
    {
      "title": "Why Japan Still Uses Cash",
      "hook": "Japan is surprisingly cash-heavy.",
      "script": "...",
      "thumbnail": "Japan still loves cash",
      "broll": [
        "Convenience store payment",
        "Tokyo train station",
        "Cash register"
      ]
    }
  ]
}
```

---

## /posts

Generate HTML preview pages for daily content.

Each HTML page should contain:

* Topic list
* Script preview
* Thumbnail text
* Suggested B-roll
* Production notes
* Source links

The HTML should:

* Be clean
* Minimal
* Mobile-friendly
* Easy to skim quickly

---

## /scripts

Contains automation scripts.

Example:

* generate_daily_topics.py
* generate_html_preview.py
* summarize_news.py

---

## /assets

Contains:

* Logos
* Icons
* Branding assets
* Thumbnail templates

---

# Content Generation Rules

For every topic generated:

Provide:

1. Viral title
2. Thumbnail text
3. 2-second hook
4. 30-second narration script
5. Suggested B-roll footage
6. Editing suggestions
7. Estimated production difficulty
8. Copyright safety notes

---

# Tone Rules

The scripts should:

* Feel natural
* Avoid exaggerated AI writing
* Avoid clickbait spam
* Feel like a real person talking
* Be emotionally engaging
* Use curiosity-driven openings

Good:
"Living in Japan, this surprised me."

Bad:
"You WON'T BELIEVE what happened in Japan!!!"

---

# Copyright & Content Safety Rules

DO NOT:

* Re-upload copyrighted news videos directly
* Copy articles word-for-word
* Reuse TV clips extensively

ALWAYS:

* Add commentary
* Transform content
* Use short reference clips only when necessary
* Prefer royalty-free B-roll
* Prefer original observations

Preferred sources:

* Pexels
* Pixabay
* Personal Tokyo footage
* Screenshots with commentary
* Public articles

---

# Shorts Structure

Recommended structure:

0-2 seconds:
Strong curiosity hook

3-15 seconds:
Context + explanation

15-25 seconds:
Insight or emotional point

25-35 seconds:
Closing thought

---

# Content Categories

Main categories:

1. Tokyo Lifestyle
2. Japanese Work Culture
3. Japanese Consumer Trends
4. AI & Technology in Japan
5. Tokyo Daily Observations
6. Japanese Social Behavior
7. Convenience Store Culture
8. Quiet Cultural Differences

---

# Production Philosophy

This is NOT a traditional news channel.

This is:
"Tokyo observations from someone living inside the system."

The content should feel:

* Personal
* Reflective
* Efficient to produce
* Sustainable long-term

---

# Daily Workflow

1. Collect topics
2. Select top 3-5
3. Generate scripts
4. Generate HTML preview
5. Review locally
6. Produce Shorts in CapCut
7. Upload to YouTube

---

# HTML Preview Requirements

The generated HTML should:

* Show all topics cleanly
* Include thumbnail previews
* Be visually minimal
* Use soft Tokyo-inspired aesthetics
* Support quick scanning

---

# Important Philosophy

Do not optimize for perfection.

Optimize for:

* consistency
* repetition
* sustainable production
* emotional resonance
* fast experimentation

# Daily Topic Collection Rules

Every morning:
1. Check Yahoo Japan News
2. Check ITmedia
3. Check Nikkei Trend
4. Check trending Japanese social topics

Select topics that:
- can be explained in under 30 seconds
- trigger curiosity
- relate to modern Japanese life
- feel emotionally interesting
- are easy to visualize with B-roll

Avoid:
- overly political topics
- complex financial analysis
- celebrity gossip without insight
- topics that require heavy research

The perspective should always be:
"Interesting observations from daily life in Japan."