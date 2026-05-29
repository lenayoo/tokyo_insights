#!/usr/bin/env python3
"""Generate a single-page Tokyo Insight dashboard for daily Shorts production."""

from __future__ import annotations

import html
import json
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
INDEX_FILE = ROOT / "index.html"


def sample_topics() -> list[dict]:
    return [
        {
            "title": "도쿄 편의점이 슈퍼마켓처럼 바뀌는 이유",
            "hook": "도쿄에서는 편의점이 이제 장보는 곳이 되어가고 있습니다.",
            "script": (
                "도쿄에 살면서 요즘 가장 현실적으로 느끼는 변화 중 하나는 편의점의 역할입니다. "
                "예전에는 급할 때 들르는 곳이었다면, 지금은 작은 슈퍼처럼 일상 장보기를 대신하는 분위기가 더 강해졌습니다. "
                "1인 가구가 많고, 멀리 큰 마트까지 가기엔 시간이 애매한 도시에서는 이런 변화가 아주 자연스럽습니다. "
                "일본의 변화는 대개 조용하게 오는데, 편의점 진열대가 바뀌는 방식은 지금 도쿄의 생활 리듬이 어떻게 달라지는지를 꽤 정확하게 보여줍니다."
            ),
            "thumbnail_text": "편의점이 장보는 곳?",
            "broll": [
                "주택가 근처 편의점 외관",
                "채소나 반찬류 진열 클로즈업",
                "작은 장바구니를 든 사람들",
                "역 앞 상점가 워킹샷",
            ],
        },
        {
            "title": "일본 정부 문서를 AI가 먼저 쓰기 시작했다",
            "hook": "일본의 AI 변화는 스타트업보다 행정에서 먼저 보이고 있습니다.",
            "script": (
                "많은 사람이 일본의 AI를 말할 때 로봇부터 떠올리지만, 실제로는 훨씬 더 조용한 곳에서 변화가 시작되고 있습니다. "
                "정부 문서 초안 작성이나 자료 정리 같은 행정 업무에 AI가 이미 들어가기 시작한 겁니다. "
                "도쿄에서 이 흐름이 흥미로운 이유는, 일본은 새로운 기술도 대개 화려하게 밀어붙이기보다 시스템 안쪽부터 천천히 스며들게 만들기 때문입니다. "
                "결국 일본의 AI 전환은 멋진 데모보다 문서, 규정, 업무 흐름에서 먼저 체감될 가능성이 큽니다."
            ),
            "thumbnail_text": "정부 문서도 AI?",
            "broll": [
                "카스미가세키 건물 외관",
                "문서와 키보드 클로즈업",
                "오피스 출근 인파",
                "노트북 화면 위 손 움직임",
            ],
        },
        {
            "title": "일본에서도 '조용한 퇴사'가 보이기 시작했다",
            "hook": "야근 문화로 유명한 일본에서도 일에 대한 거리두기가 보이기 시작했습니다.",
            "script": (
                "일본에서 일 이야기를 할 때 보통은 과로와 인내를 떠올리지만, 요즘은 조금 다른 공기도 느껴집니다. "
                "겉으로 크게 불만을 말하지는 않지만, 승진이나 과도한 헌신에서 한 발 물러서는 사람들이 늘고 있다는 점입니다. "
                "일본에서는 변화가 늘 천천히 보이기 때문에 이런 흐름은 더 의미가 있습니다. "
                "예전처럼 회사가 삶의 중심이어야 한다는 감각이 약해지고 있고, 사람들은 조용하게 자기 일과 삶의 경계를 다시 그리고 있는 것처럼 보입니다."
            ),
            "thumbnail_text": "일본의 조용한 퇴사",
            "broll": [
                "아침 출근길 역 인파",
                "사무실 빌딩 엘리베이터 앞",
                "노트북을 덮는 손",
                "퇴근 후 조용한 주택가 골목",
            ],
        },
        {
            "title": "일본 소비 트렌드가 '시간 절약'에서 '마음 보호'로 이동 중이다",
            "hook": "이제는 빠른 것보다 덜 지치는 소비가 더 중요해지고 있습니다.",
            "script": (
                "도쿄 생활을 하다 보면 효율적인 도시라는 말을 자주 떠올리게 되지만, 동시에 꽤 지치는 도시이기도 합니다. "
                "그래서 요즘 일본 소비에서 흥미로운 건, 시간을 아끼는 것보다 마음이 덜 소모되는 경험을 찾는 흐름입니다. "
                "선택지가 너무 많지 않고, 비교 피로가 적고, 들어가면 바로 이해되는 매장이나 서비스가 더 매력적으로 보이는 거죠. "
                "결국 앞으로는 더 빠른 서비스보다 덜 피곤한 서비스가 프리미엄이 될 수도 있다는 얘기인데, 이건 도쿄 같은 도시에서 특히 설득력이 있습니다."
            ),
            "thumbnail_text": "덜 지치는 소비",
            "broll": [
                "복잡한 진열대와 가격표",
                "조용한 카페나 서점 내부",
                "선택 앞에서 멈춘 손",
                "도쿄 번화가 워킹샷",
            ],
        },
        {
            "title": "AI 안경이 일본에 들어오면 가장 먼저 시험대가 되는 곳은 도쿄다",
            "hook": "도쿄는 AI 안경이 정말 유용한지 바로 드러나는 도시입니다.",
            "script": (
                "AI 안경 이야기를 들으면 미래적인 제품처럼 느껴지지만, 도쿄에서는 꽤 현실적인 도구가 될 수도 있습니다. "
                "이 도시는 간판, 메뉴, 역 안내, 작은 글씨가 끝없이 이어지는 곳이라 시선이 늘 바쁩니다. "
                "그래서 번역이나 정보 보조가 눈앞에서 바로 이뤄진다면, 도쿄에서는 그 효용이 아주 빨리 드러날 수 있습니다. "
                "중요한 건 기술의 화려함보다 일상에 자연스럽게 섞이느냐인데, 그런 의미에서 도쿄는 AI 안경의 가장 정직한 테스트 장소처럼 보입니다."
            ),
            "thumbnail_text": "도쿄에서 AI 안경",
            "broll": [
                "시부야나 신주쿠 POV 워킹샷",
                "간판과 메뉴판 클로즈업",
                "안경을 손에 든 컷",
                "도심 인파 와이드샷",
            ],
        },
    ]


def build_payload(target_date: str) -> dict:
    return {"date": target_date, "topics": sample_topics()}


def normalize_topic(topic: dict) -> dict:
    broll = topic.get("broll")
    if not broll:
        broll = topic.get("broll_suggestions", [])

    script = topic.get("script")
    if not script:
        script = topic.get("30_second_script", "")

    return {
        "title": str(topic.get("title", "")).strip(),
        "hook": str(topic.get("hook", "")).strip(),
        "script": str(script).strip(),
        "thumbnail_text": str(
            topic.get("thumbnail_text", topic.get("thumbnail", ""))
        ).strip(),
        "broll": [str(item).strip() for item in broll if str(item).strip()],
    }


def normalize_payload(payload: dict, target_date: str) -> dict:
    topics = []
    for raw_topic in payload.get("topics", []):
        topic = normalize_topic(raw_topic)
        if topic["title"]:
            topics.append(topic)

    return {
        "date": str(payload.get("date", target_date)),
        "topics": topics,
    }


def load_payload(path: Path, target_date: str) -> dict:
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        payload = build_payload(target_date)
    return normalize_payload(payload, target_date)


def load_archives() -> list[dict]:
    archives = []
    for path in sorted(DATA_DIR.glob("*.json"), reverse=True):
        payload = json.loads(path.read_text(encoding="utf-8"))
        archives.append(normalize_payload(payload, path.stem))
    return archives


def korean_date(value: str) -> str:
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return f"{parsed.year}년 {parsed.month}월 {parsed.day}일"


def chip_date(value: str) -> str:
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return f"{parsed.month:02d}.{parsed.day:02d}"


def page_styles() -> str:
    return """
    :root {
      --bg: #f4efe7;
      --bg-accent: #ebe3d6;
      --paper: rgba(255, 252, 247, 0.92);
      --paper-strong: rgba(255, 250, 244, 0.98);
      --ink: #1d272c;
      --muted: #67747a;
      --line: rgba(29, 39, 44, 0.1);
      --accent: #c4633f;
      --accent-soft: rgba(196, 99, 63, 0.12);
      --shadow: 0 18px 42px rgba(35, 31, 28, 0.08);
      --radius: 20px;
      --radius-small: 14px;
      --max: 1120px;
      --sans: "Hiragino Sans", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif;
    }

    * {
      box-sizing: border-box;
    }

    html {
      background:
        radial-gradient(circle at top left, rgba(196, 99, 63, 0.12), transparent 32%),
        linear-gradient(180deg, #faf6ef 0%, var(--bg) 48%, var(--bg-accent) 100%);
      color: var(--ink);
      font-family: var(--sans);
      line-height: 1.6;
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      min-height: 100vh;
    }

    button,
    textarea {
      font: inherit;
    }

    .shell {
      width: min(calc(100% - 24px), var(--max));
      margin: 0 auto;
      padding: 20px 0 48px;
    }

    .topbar,
    .date-rail,
    .day-panel,
    .topic-card {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }

    .topbar {
      padding: 22px;
      margin-bottom: 14px;
    }

    .eyebrow {
      margin: 0 0 8px;
      color: var(--accent);
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }

    h1,
    h2,
    h3 {
      margin: 0;
      line-height: 1.2;
    }

    h1 {
      font-size: clamp(1.8rem, 5vw, 3.4rem);
      letter-spacing: -0.03em;
      margin-bottom: 10px;
    }

    h2 {
      font-size: clamp(1.3rem, 3vw, 1.9rem);
    }

    h3 {
      font-size: 1.1rem;
      letter-spacing: -0.02em;
    }

    p {
      margin: 0;
    }

    .lead {
      color: var(--muted);
      max-width: 56ch;
    }

    .date-rail {
      position: sticky;
      top: 10px;
      z-index: 5;
      padding: 14px;
      margin-bottom: 14px;
    }

    .date-scroll {
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding-bottom: 2px;
      scrollbar-width: none;
    }

    .date-scroll::-webkit-scrollbar {
      display: none;
    }

    .date-tab {
      display: inline-flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 2px;
      min-width: 102px;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--paper-strong);
      color: var(--ink);
      cursor: pointer;
      transition: border-color 140ms ease, transform 140ms ease, background 140ms ease;
    }

    .date-tab:hover {
      transform: translateY(-1px);
      border-color: rgba(29, 39, 44, 0.22);
    }

    .date-tab.is-active {
      background: var(--accent-soft);
      border-color: rgba(196, 99, 63, 0.3);
      color: var(--accent);
    }

    .date-tab strong {
      font-size: 0.98rem;
    }

    .date-tab span {
      font-size: 0.78rem;
      color: var(--muted);
    }

    .date-tab.is-active span {
      color: rgba(196, 99, 63, 0.84);
    }

    .day-panel {
      padding: 20px;
    }

    .day-panel[hidden] {
      display: none;
    }

    .day-header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 12px;
      margin-bottom: 18px;
    }

    .day-meta {
      color: var(--muted);
      font-size: 0.95rem;
    }

    .day-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .ghost-button,
    .copy-button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 9px 14px;
      background: var(--paper-strong);
      color: var(--ink);
      cursor: pointer;
      text-decoration: none;
    }

    .ghost-button:hover,
    .copy-button:hover {
      border-color: rgba(29, 39, 44, 0.22);
    }

    .topic-list {
      display: grid;
      gap: 14px;
    }

    .topic-card {
      padding: 18px;
    }

    .topic-head {
      display: flex;
      gap: 12px;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .topic-number {
      flex: 0 0 auto;
      width: 32px;
      height: 32px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 700;
      font-size: 0.92rem;
    }

    .hook {
      margin-top: 10px;
      padding: 12px 14px;
      border-left: 3px solid var(--accent);
      border-radius: 0 12px 12px 0;
      background: rgba(196, 99, 63, 0.08);
      color: var(--ink);
    }

    .topic-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
      margin-top: 14px;
    }

    .block {
      border: 1px solid var(--line);
      border-radius: var(--radius-small);
      background: rgba(255, 255, 255, 0.55);
      padding: 14px;
    }

    .label {
      display: inline-block;
      margin-bottom: 8px;
      color: var(--accent);
      font-size: 0.74rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    .thumbnail-chip {
      display: inline-flex;
      align-items: center;
      padding: 8px 11px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-weight: 700;
    }

    .script-wrap {
      display: grid;
      gap: 10px;
    }

    .script-box {
      width: 100%;
      min-height: 150px;
      resize: vertical;
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: var(--radius-small);
      background: rgba(255, 255, 255, 0.86);
      color: var(--ink);
      line-height: 1.65;
    }

    .script-box:focus {
      outline: 2px solid rgba(196, 99, 63, 0.18);
      border-color: rgba(196, 99, 63, 0.28);
    }

    ul {
      margin: 0;
      padding-left: 18px;
    }

    li + li {
      margin-top: 6px;
    }

    .small {
      color: var(--muted);
      font-size: 0.92rem;
    }

    .empty {
      padding: 28px;
      text-align: center;
      color: var(--muted);
    }

    @media (min-width: 760px) {
      .topic-grid.two-col {
        grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
      }
    }

    @media (max-width: 640px) {
      .shell {
        width: min(calc(100% - 16px), var(--max));
        padding-top: 14px;
      }

      .topbar,
      .date-rail,
      .day-panel,
      .topic-card {
        padding: 16px;
      }

      .date-tab {
        min-width: 88px;
      }
    }
    """


def render_list(items: list[str]) -> str:
    entries = "\n".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul>{entries}</ul>"


def render_topic(topic: dict, topic_index: int, day_index: int) -> str:
    script_id = f"script-{day_index}-{topic_index}"
    return f"""
        <article class="topic-card">
          <div class="topic-head">
            <span class="topic-number">{topic_index}</span>
            <div>
              <h3>{html.escape(topic["title"])}</h3>
              <p class="hook">{html.escape(topic["hook"])}</p>
            </div>
          </div>

          <div class="topic-grid two-col">
            <section class="block">
              <span class="label">스크립트</span>
              <div class="script-wrap">
                <p class="small">클릭해서 바로 선택하거나 복사 버튼으로 가져가면 됩니다.</p>
                <textarea
                  class="script-box"
                  id="{script_id}"
                  readonly
                  spellcheck="false"
                  onclick="this.focus();this.select();"
                >{html.escape(topic["script"])}</textarea>
                <div>
                  <button class="copy-button" type="button" data-copy-target="{script_id}">스크립트 복사</button>
                </div>
              </div>
            </section>

            <div class="topic-grid">
              <section class="block">
                <span class="label">썸네일 문구</span>
                <div class="thumbnail-chip">{html.escape(topic["thumbnail_text"])}</div>
              </section>

              <section class="block">
                <span class="label">브롤</span>
                {render_list(topic["broll"])}
              </section>
            </div>
          </div>
        </article>
    """


def render_day_panel(payload: dict, day_index: int, active: bool) -> str:
    panel_id = f"day-{payload['date']}"
    bundle = "\n\n".join(
        f"{index}. {topic['title']}\n{topic['script']}"
        for index, topic in enumerate(payload["topics"], start=1)
    )
    bundle_id = f"bundle-{day_index}"
    topics_html = "\n".join(
        render_topic(topic, topic_index, day_index)
        for topic_index, topic in enumerate(payload["topics"], start=1)
    )
    hidden_attr = "" if active else " hidden"
    return f"""
      <section class="day-panel" id="{panel_id}"{hidden_attr}>
        <div class="day-header">
          <div>
            <p class="eyebrow">Daily Shorts Board</p>
            <h2>{html.escape(korean_date(payload["date"]))}</h2>
            <p class="day-meta">{len(payload["topics"])}개 주제. 도쿄에서 바로 찍고 바로 쓰기 좋게 정리했습니다.</p>
          </div>
          <div class="day-actions">
            <button class="ghost-button" type="button" data-copy-bundle-target="{bundle_id}">하루 스크립트 복사</button>
          </div>
        </div>
        <textarea id="{bundle_id}" hidden>{html.escape(bundle)}</textarea>
        <div class="topic-list">
          {topics_html}
        </div>
      </section>
    """


def render_index_html(archives: list[dict]) -> str:
    if not archives:
        day_panels = '<section class="day-panel"><div class="empty">아직 생성된 날짜가 없습니다.</div></section>'
        date_tabs = ""
    else:
        day_panels = "\n".join(
            render_day_panel(payload, day_index, active=(day_index == 0))
            for day_index, payload in enumerate(archives)
        )
        date_tabs = "\n".join(
            f"""
            <button class="date-tab{' is-active' if day_index == 0 else ''}" type="button" data-target="day-{payload['date']}">
              <strong>{html.escape(chip_date(payload["date"]))}</strong>
              <span>{len(payload["topics"])}개 주제</span>
            </button>
            """
            for day_index, payload in enumerate(archives)
        )

    return f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tokyo Insight</title>
    <style>{page_styles()}</style>
  </head>
  <body>
    <main class="shell">
      <header class="topbar">
        <p class="eyebrow">Tokyo Insight</p>
        <h1>도쿄에 사는 한국인 크리에이터의 숏츠 작업 보드</h1>
        <p class="lead">
          날짜를 누르면 바로 훅, 스크립트, 썸네일 문구, 브롤이 펼쳐집니다.
          뉴스보다 관찰에 가깝고, 완성도보다 반복 가능한 생산 속도에 맞췄습니다.
        </p>
      </header>

      <section class="date-rail">
        <div class="date-scroll">
          {date_tabs}
        </div>
      </section>

      {day_panels}
    </main>

    <script>
      const tabs = Array.from(document.querySelectorAll(".date-tab"));
      const panels = Array.from(document.querySelectorAll(".day-panel[id]"));

      function activatePanel(targetId) {{
        tabs.forEach((tab) => {{
          tab.classList.toggle("is-active", tab.dataset.target === targetId);
        }});
        panels.forEach((panel) => {{
          panel.hidden = panel.id !== targetId;
        }});
        const activePanel = document.getElementById(targetId);
        if (activePanel) {{
          activePanel.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }}
      }}

      tabs.forEach((tab) => {{
        tab.addEventListener("click", () => activatePanel(tab.dataset.target));
      }});

      async function copyText(text) {{
        try {{
          await navigator.clipboard.writeText(text);
          return true;
        }} catch (error) {{
          const helper = document.createElement("textarea");
          helper.value = text;
          document.body.appendChild(helper);
          helper.select();
          const copied = document.execCommand("copy");
          document.body.removeChild(helper);
          return copied;
        }}
      }}

      document.querySelectorAll("[data-copy-target]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          const field = document.getElementById(button.dataset.copyTarget);
          if (!field) return;
          const ok = await copyText(field.value);
          if (!ok) return;
          const original = button.textContent;
          button.textContent = "복사됨";
          window.setTimeout(() => {{
            button.textContent = original;
          }}, 1200);
        }});
      }});

      document.querySelectorAll("[data-copy-bundle-target]").forEach((button) => {{
        button.addEventListener("click", async () => {{
          const field = document.getElementById(button.dataset.copyBundleTarget);
          if (!field) return;
          const ok = await copyText(field.value);
          if (!ok) return;
          const original = button.textContent;
          button.textContent = "하루분 복사됨";
          window.setTimeout(() => {{
            button.textContent = original;
          }}, 1200);
        }});
      }});
    </script>
  </body>
</html>
"""


def ensure_directories() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def write_json_file(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_directories()

    target_date = date.today().isoformat()
    json_path = DATA_DIR / f"{target_date}.json"

    payload = load_payload(json_path, target_date)
    write_json_file(json_path, payload)

    archives = load_archives()
    write_text_file(INDEX_FILE, render_index_html(archives))

    print(f"생성 완료: {json_path.relative_to(ROOT)}")
    print(f"갱신 완료: {INDEX_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
