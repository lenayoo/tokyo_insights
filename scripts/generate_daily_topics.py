#!/usr/bin/env python3
"""Generate sample daily topic data and HTML previews for Tokyo Insight."""

from __future__ import annotations

import html
import json
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
POSTS_DIR = ROOT / "posts"
INDEX_FILE = ROOT / "index.html"


def sample_topics() -> list[dict]:
    return [
        {
            "category": "Convenience Store Culture",
            "title": "Why Tokyo convenience stores feel strangely calm",
            "thumbnail_text": "Tokyo conbini calm",
            "hook": "Living in Tokyo, even convenience stores feel quiet.",
            "30_second_script": (
                "One thing that still stands out to me in Tokyo is how calm a convenience "
                "store can feel. People move fast, but not loudly. The shelves are precise, "
                "the lighting is soft, and even late at night it feels organized instead of "
                "chaotic. It says something bigger about daily life here. Efficiency in Japan "
                "often looks gentle on the surface, even when the system behind it is intense."
            ),
            "broll_suggestions": [
                "Store exterior at dusk",
                "Neatly arranged shelves",
                "Coffee machine or cashier counter",
                "Pedestrians passing a lit conbini",
            ],
            "editing_notes": [
                "Open with a slow exterior shot, then cut into handheld shelf details.",
                "Use text overlays for key words: calm, precise, efficient.",
            ],
            "source_ideas": [
                "Original footage of a neighborhood convenience store exterior at night",
                "Pexels search for Tokyo street or convenience store style B-roll",
                "Personal walking footage near a station or residential area",
            ],
            "copyright_risk": (
                "Low if you use your own footage or royalty-free city clips. Avoid TV clips or store-owned promo videos."
            ),
            "production_difficulty": "Low",
        },
        {
            "category": "Japanese Consumer Trends",
            "title": "Why cash still appears everywhere in Japan",
            "thumbnail_text": "Japan still uses cash",
            "hook": "Japan feels high-tech, but cash is still everywhere.",
            "30_second_script": (
                "People outside Japan often imagine a fully cashless country, but daily life "
                "here tells a different story. You can pay by phone in many places, but cash "
                "still shows up constantly in cafes, small restaurants, and older local shops. "
                "It is not just about technology. It is also habit, trust, and the way older "
                "systems stay alive much longer in Japan than you might expect."
            ),
            "broll_suggestions": [
                "Coins and bills on a tray",
                "Train station ticket machine",
                "Small restaurant register",
                "Wallet close-up in a cafe",
            ],
            "editing_notes": [
                "Cut between cash and smartphone payment to show contrast.",
                "Use a clean subtitle line for the insight: habit can outlast technology.",
            ],
            "source_ideas": [
                "Original payment or wallet close-up footage without showing private details",
                "Personal Tokyo cafe or restaurant counter footage",
                "Government or public statistics pages for background context only",
            ],
            "copyright_risk": (
                "Low if you film your own hands, wallet, or payment tray. Avoid showing private customer data or reusing news footage."
            ),
            "production_difficulty": "Low",
        },
        {
            "category": "Japanese Work Culture",
            "title": "The quiet pressure hidden inside Tokyo offices",
            "thumbnail_text": "Quiet pressure in Tokyo",
            "hook": "Tokyo offices can look calm even when the pressure is not.",
            "30_second_script": (
                "What surprised me about work culture in Japan is that stress is not always loud. "
                "In some offices, the room stays quiet, people stay polite, and everything looks "
                "controlled. But underneath that, there can still be strong pressure to read the "
                "room, avoid friction, and keep the group moving smoothly. The intensity is real. "
                "It is just expressed in a more restrained way."
            ),
            "broll_suggestions": [
                "Morning office buildings",
                "Commuters entering a station",
                "Laptop and notebook on a desk",
                "Elevator or hallway shots",
            ],
            "editing_notes": [
                "Start with silent office visuals before the narration enters.",
                "Keep the pacing slower than a typical news short to match the tone.",
            ],
            "source_ideas": [
                "Original commuter footage around office districts or stations",
                "Royalty-free office building shots for atmosphere",
                "Personal desk setup shots instead of filming real office interiors",
            ],
            "copyright_risk": (
                "Medium because workplace footage can expose private spaces or people. Favor public exteriors and generic desk visuals."
            ),
            "production_difficulty": "Medium",
        },
        {
            "category": "AI & Technology in Japan",
            "title": "What AI in Tokyo actually looks like day to day",
            "thumbnail_text": "AI in Tokyo is quieter",
            "hook": "AI in Tokyo feels quieter than people imagine.",
            "30_second_script": (
                "When people talk about AI in Japan, they often expect robots everywhere. "
                "But the more realistic story in Tokyo is much quieter. AI shows up in office "
                "tools, customer support, translation, scheduling, and retail experiments. "
                "It is less futuristic theater and more background infrastructure. That is what "
                "makes it interesting. The change is steady, practical, and easy to miss if you only look for spectacle."
            ),
            "broll_suggestions": [
                "Laptop with coding or dashboard screens",
                "Digital signage in a station",
                "People using self-service kiosks",
                "Wide city shot with trains or offices",
            ],
            "editing_notes": [
                "Mix wide Tokyo city shots with practical close-ups of screens and kiosks.",
                "Use restrained captions instead of flashy effects.",
            ],
            "source_ideas": [
                "Original footage of kiosks, signs, or screens in public spaces",
                "Personal laptop or coding footage for abstract AI visuals",
                "Public company product pages used briefly as visual reference with commentary",
            ],
            "copyright_risk": (
                "Medium if you show branded product screens for too long. Keep clips short and heavily commentary-driven."
            ),
            "production_difficulty": "Medium",
        },
    ]


def build_payload(target_date: str) -> dict:
    return {
        "date": target_date,
        "channel": "Tokyo Insight",
        "perspective": "A Korean developer living in Tokyo observing Japanese society from the inside.",
        "topics": sample_topics(),
    }


def formatted_date(value: str) -> str:
    return datetime.strptime(value, "%Y-%m-%d").strftime("%B %d, %Y")


def page_styles() -> str:
    return """
    :root {
      --bg: #f6f1e8;
      --bg-soft: #fdfaf4;
      --paper: rgba(255, 252, 247, 0.88);
      --paper-strong: rgba(255, 250, 242, 0.97);
      --ink: #1f2a30;
      --muted: #627077;
      --line: rgba(31, 42, 48, 0.12);
      --accent: #be6a4a;
      --accent-soft: rgba(190, 106, 74, 0.12);
      --accent-cool: #6d8b8a;
      --shadow: 0 24px 60px rgba(42, 36, 31, 0.08);
      --radius: 22px;
      --radius-small: 14px;
      --max: 1080px;
      --sans: "Avenir Next", "Segoe UI", sans-serif;
      --serif: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
    }

    * {
      box-sizing: border-box;
    }

    html {
      background:
        radial-gradient(circle at top left, rgba(190, 106, 74, 0.14), transparent 32%),
        radial-gradient(circle at top right, rgba(109, 139, 138, 0.15), transparent 28%),
        linear-gradient(180deg, #faf6ef 0%, var(--bg) 52%, #efe7dc 100%);
      color: var(--ink);
      font-family: var(--sans);
      line-height: 1.65;
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      min-height: 100vh;
    }

    a {
      color: inherit;
    }

    .shell {
      width: min(calc(100% - 32px), var(--max));
      margin: 0 auto;
      padding: 32px 0 64px;
    }

    .hero,
    .panel,
    .topic-card,
    .archive-card {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }

    .hero {
      padding: 28px;
      margin-bottom: 22px;
    }

    .eyebrow {
      color: var(--accent);
      font-size: 0.78rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      margin: 0 0 10px;
    }

    h1,
    h2,
    h3 {
      font-family: var(--serif);
      line-height: 1.15;
      margin: 0;
    }

    h1 {
      font-size: clamp(2.2rem, 6vw, 4.4rem);
      margin-bottom: 10px;
    }

    h2 {
      font-size: clamp(1.4rem, 3vw, 2rem);
      margin-bottom: 16px;
    }

    h3 {
      font-size: 1.2rem;
      margin-bottom: 12px;
    }

    p {
      margin: 0 0 14px;
    }

    .lead {
      color: var(--muted);
      font-size: 1.05rem;
      max-width: 64ch;
    }

    .meta,
    .pill-row,
    .actions,
    .stats,
    .archive-grid,
    .topic-grid,
    .detail-grid,
    .steps {
      display: grid;
      gap: 14px;
    }

    .actions,
    .pill-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 20px;
    }

    .action {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--paper-strong);
      text-decoration: none;
      color: var(--ink);
    }

    .action:hover {
      border-color: rgba(31, 42, 48, 0.24);
      transform: translateY(-1px);
    }

    .panel {
      padding: 24px;
      margin-bottom: 22px;
    }

    .steps,
    .archive-grid {
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }

    .step,
    .archive-card {
      padding: 18px;
      border-radius: var(--radius-small);
      background: var(--paper-strong);
      border: 1px solid var(--line);
    }

    .archive-card h3 {
      margin-bottom: 6px;
    }

    .topic-grid {
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      margin-top: 16px;
    }

    .topic-link {
      display: block;
      text-decoration: none;
      padding: 16px;
      border-radius: var(--radius-small);
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0.28));
    }

    .topic-link:hover {
      border-color: rgba(31, 42, 48, 0.24);
      transform: translateY(-1px);
    }

    .topic-card {
      padding: 24px;
      margin-bottom: 18px;
    }

    .detail-grid {
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      margin-top: 18px;
    }

    .detail {
      padding: 16px;
      border-radius: var(--radius-small);
      background: rgba(255, 255, 255, 0.52);
      border: 1px solid var(--line);
    }

    .label {
      display: inline-block;
      margin-bottom: 10px;
      color: var(--accent);
      font-size: 0.76rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      padding: 7px 11px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 0.86rem;
      text-decoration: none;
    }

    ul {
      margin: 0;
      padding-left: 18px;
    }

    li + li {
      margin-top: 6px;
    }

    .muted {
      color: var(--muted);
    }

    .archive-meta,
    .small {
      color: var(--muted);
      font-size: 0.94rem;
    }

    .quote {
      padding: 16px 18px;
      border-left: 3px solid var(--accent-cool);
      background: rgba(109, 139, 138, 0.08);
      border-radius: 0 14px 14px 0;
    }

    .copy-box {
      width: 100%;
      min-height: 180px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: var(--radius-small);
      background: rgba(255, 255, 255, 0.82);
      color: var(--ink);
      font: inherit;
      line-height: 1.6;
      resize: vertical;
    }

    .copy-box:focus {
      outline: 2px solid rgba(109, 139, 138, 0.28);
      border-color: rgba(109, 139, 138, 0.44);
    }

    footer {
      margin-top: 28px;
      color: var(--muted);
      font-size: 0.95rem;
    }

    @media (max-width: 640px) {
      .shell {
        width: min(calc(100% - 20px), var(--max));
        padding-top: 20px;
      }

      .hero,
      .panel,
      .topic-card {
        padding: 20px;
      }

      h1 {
        font-size: 2.1rem;
      }
    }
    """


def render_list(items: list[str]) -> str:
    entries = "\n".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul>{entries}</ul>"


def render_source_links(links: list[dict]) -> str:
    entries = "\n".join(
        (
            "<li>"
            f"<a href=\"{html.escape(link['url'])}\" target=\"_blank\" rel=\"noreferrer\">"
            f"{html.escape(link['label'])}</a>"
            "</li>"
        )
        for link in links
    )
    return f"<ul>{entries}</ul>"


def render_copy_box(text: str) -> str:
    return (
        "<textarea class=\"copy-box\" readonly rows=\"8\" spellcheck=\"false\" "
        "onclick=\"this.focus();this.select();\">"
        f"{html.escape(text)}"
        "</textarea>"
    )


def render_post_html(payload: dict) -> str:
    target_date = payload["date"]
    long_date = formatted_date(target_date)
    topics = payload["topics"]
    indexed_topics = list(enumerate(topics, start=1))
    ranked_topics = sorted(
        (
            (index, topic)
            for index, topic in indexed_topics
            if topic.get("top_5_rank") is not None
        ),
        key=lambda item: item[1]["top_5_rank"],
    )

    topic_nav = "\n".join(
        (
            f"<a class=\"topic-link\" href=\"#topic-{index}\">"
            f"<span class=\"label\">{html.escape(topic['category'])}</span>"
            f"<h3>{html.escape(topic['title'])}</h3>"
            f"<p class=\"small\">{html.escape(topic['hook'])}</p>"
            "</a>"
        )
        for index, topic in indexed_topics
    )

    top_five_panel = ""
    if ranked_topics:
        ranked_nav = "\n".join(
            (
                f"<a class=\"topic-link\" href=\"#topic-{index}\">"
                f"<span class=\"label\">Top 5 #{html.escape(str(topic['top_5_rank']))}</span>"
                f"<h3>{html.escape(topic['title'])}</h3>"
                f"<p class=\"small\">{html.escape(topic['hook'])}</p>"
                "</a>"
            )
            for index, topic in ranked_topics
        )
        top_five_panel = f"""
      <section class="panel">
        <h2>Top 5 Today</h2>
        <p class="muted">These are the five topics to prioritize if you only produce a few Shorts.</p>
        <div class="topic-grid">
          {ranked_nav}
        </div>
      </section>
"""

    topic_cards = []
    for index, topic in indexed_topics:
        rank_pill = (
            f"<span class=\"pill\">Top 5 #{html.escape(str(topic['top_5_rank']))}</span>"
            if topic.get("top_5_rank") is not None
            else "<span class=\"pill\">Watchlist</span>"
        )
        source_links_html = ""
        if topic.get("source_links"):
            source_links_html = f"""
              <section class="detail" style="margin-top: 18px;">
                <span class="label">Source Links</span>
                {render_source_links(topic["source_links"])}
              </section>
            """
        topic_cards.append(
            f"""
            <article class="topic-card" id="topic-{index}">
              <p class="eyebrow">Topic {index}</p>
              <h2>{html.escape(topic["title"])}</h2>
              <div class="pill-row">
                <span class="pill">{html.escape(topic["category"])}</span>
                {rank_pill}
                <span class="pill">Difficulty: {html.escape(topic["production_difficulty"])}</span>
              </div>
              <p class="quote">{html.escape(topic["hook"])}</p>
              <div class="detail-grid">
                <section class="detail">
                  <span class="label">Thumbnail Text</span>
                  <p>{html.escape(topic["thumbnail_text"])}</p>
                </section>
                <section class="detail">
                  <span class="label">Copyright Risk</span>
                  <p>{html.escape(topic["copyright_risk"])}</p>
                </section>
              </div>
              <section class="detail" style="margin-top: 18px;">
                <span class="label">30 Second Script</span>
                <p class="small">Click inside the box to select the full script for CapCut.</p>
                {render_copy_box(topic["30_second_script"])}
              </section>
              <div class="detail-grid">
                <section class="detail">
                  <span class="label">B-roll Suggestions</span>
                  {render_list(topic["broll_suggestions"])}
                </section>
                <section class="detail">
                  <span class="label">Editing Notes</span>
                  {render_list(topic["editing_notes"])}
                </section>
              </div>
              <section class="detail" style="margin-top: 18px;">
                <span class="label">Source Ideas</span>
                {render_list(topic["source_ideas"])}
              </section>
              {source_links_html}
            </article>
            """
        )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tokyo Insight | {html.escape(target_date)}</title>
    <style>{page_styles()}</style>
  </head>
  <body>
    <main class="shell">
      <section class="hero">
        <p class="eyebrow">Tokyo Insight Daily Preview</p>
        <h1>{html.escape(long_date)}</h1>
        <p class="lead">{html.escape(payload["perspective"])}</p>
        <div class="actions">
          <a class="action" href="../index.html">Back to homepage</a>
          <a class="action" href="../data/{html.escape(target_date)}.json">Open JSON data</a>
        </div>
      </section>

      <section class="panel">
        <h2>Topic Lineup</h2>
        <p class="muted">Designed for quick scanning before production.</p>
        <div class="topic-grid">
          {topic_nav}
        </div>
      </section>

      {top_five_panel}

      {''.join(topic_cards)}

      <footer>
        Generated locally from <code>scripts/generate_daily_topics.py</code>.
      </footer>
    </main>
  </body>
</html>
"""


def load_archives() -> list[dict]:
    archives = []
    for path in sorted(DATA_DIR.glob("*.json"), reverse=True):
        payload = json.loads(path.read_text(encoding="utf-8"))
        topics = payload.get("topics", [])
        archives.append(
            {
                "date": payload.get("date", path.stem),
                "topic_count": len(topics),
                "titles": [topic.get("title", "Untitled") for topic in topics[:3]],
            }
        )
    return archives


def render_index_html(archives: list[dict]) -> str:
    archive_cards = "\n".join(
        f"""
        <article class="archive-card">
          <p class="eyebrow">Daily Archive</p>
          <h3>{html.escape(formatted_date(archive["date"]))}</h3>
          <p class="archive-meta">{archive["topic_count"]} topics prepared for Shorts production.</p>
          {render_list(archive["titles"])}
          <div class="actions">
            <a class="action" href="posts/{html.escape(archive["date"])}.html">Open preview</a>
            <a class="action" href="data/{html.escape(archive["date"])}.json">Open JSON</a>
          </div>
        </article>
        """
        for archive in archives
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tokyo Insight</title>
    <style>{page_styles()}</style>
  </head>
  <body>
    <main class="shell">
      <section class="hero">
        <p class="eyebrow">Tokyo Insight</p>
        <h1>Calm Tokyo observations, built for fast Shorts.</h1>
        <p class="lead">
          A lightweight local system for turning daily Tokyo observations into scripts,
          hooks, B-roll notes, and preview pages without external dependencies.
        </p>
        <div class="actions">
          <a class="action" href="AGENTS.md">Read AGENTS.md</a>
          <a class="action" href="README.md">Read README</a>
        </div>
      </section>

      <section class="panel">
        <h2>Daily Workflow</h2>
        <div class="steps">
          <div class="step">
            <span class="label">1. Generate</span>
            <p>Run <code>python3 scripts/generate_daily_topics.py</code> to create or refresh today&apos;s files.</p>
          </div>
          <div class="step">
            <span class="label">2. Review</span>
            <p>Open the daily preview page, skim hooks, scripts, and B-roll, then choose the best 3 to 5 topics.</p>
          </div>
          <div class="step">
            <span class="label">3. Produce</span>
            <p>Record voiceover, collect clips, and move the selected topics into CapCut or your publishing workflow.</p>
          </div>
        </div>
      </section>

      <section class="panel">
        <h2>Archive</h2>
        <p class="muted">Each day produces a JSON topic file and a matching HTML preview.</p>
        <div class="archive-grid">
          {archive_cards}
        </div>
      </section>

      <footer>
        Keep editorial direction in <code>AGENTS.md</code>. Keep automation simple in <code>scripts/</code>.
      </footer>
    </main>
  </body>
</html>
"""


def ensure_directories() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    POSTS_DIR.mkdir(exist_ok=True)


def load_payload(json_path: Path, target_date: str) -> dict:
    if json_path.exists():
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    else:
        payload = build_payload(target_date)

    payload.setdefault("date", target_date)
    payload.setdefault("channel", "Tokyo Insight")
    payload.setdefault(
        "perspective",
        "A Korean developer living in Tokyo observing Japanese society from the inside.",
    )
    payload.setdefault("topics", [])
    return payload


def write_json_file(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_directories()

    target_date = date.today().isoformat()
    json_path = DATA_DIR / f"{target_date}.json"
    post_path = POSTS_DIR / f"{target_date}.html"
    payload = load_payload(json_path, target_date)

    write_json_file(json_path, payload)
    write_text_file(post_path, render_post_html(payload))
    write_text_file(INDEX_FILE, render_index_html(load_archives()))

    print(f"Generated {json_path.relative_to(ROOT)}")
    print(f"Generated {post_path.relative_to(ROOT)}")
    print(f"Updated {INDEX_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
