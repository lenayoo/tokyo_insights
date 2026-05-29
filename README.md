# Tokyo Insight

Tokyo Insight is a lightweight content system for planning YouTube Shorts about Tokyo life, Japanese culture, work habits, consumer behavior, and technology from the perspective of a Korean developer living in Tokyo.

`AGENTS.md` is the main instruction file for tone, structure, and production rules.

## What It Includes

- `data/`: daily structured topic JSON files
- `posts/`: daily HTML preview pages
- `scripts/generate_daily_topics.py`: sample generator for daily topics and previews
- `index.html`: local homepage that links to generated daily posts

## Generate Daily Topics

Run:

```bash
python3 scripts/generate_daily_topics.py
```

The script will:

1. Create or update `data/YYYY-MM-DD.json`
2. Create or update `posts/YYYY-MM-DD.html`
3. Refresh `index.html` so the new post appears on the homepage

The current version uses built-in sample topics only. No external APIs or third-party packages are required.

## Preview Posts Locally

1. Run the generator command above.
2. Open `index.html` in your browser.
3. Click the daily archive link to view the full post preview page.

Because everything uses plain HTML with relative links, opening files locally is enough.

## Add Future Automation

The easiest next extensions are inside `scripts/generate_daily_topics.py`:

- Replace `sample_topics()` with topic collection from your own sources
- Add more fields such as captions, hashtags, or shot lists
- Split HTML rendering into reusable templates if the previews grow
- Add a second script for summarizing articles or ranking topic ideas

Keep the output aligned with `AGENTS.md` so the content stays consistent with the channel voice.
# tokyo_insights
