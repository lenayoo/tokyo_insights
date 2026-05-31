# Tokyo Insight - AGENTS.md

# 프로젝트 개요

Tokyo Insight는
“도쿄에 사는 한국인 개발자의 시선으로 바라보는 일본 사회”
를 주제로 하는 YouTube Shorts 제작 시스템이다.

핵심 방향:

- 일본 문화
- 도쿄 라이프스타일
- 일본 회사 문화
- 일본 소비문화
- 일본 AI/기술
- 생활 속 작은 문화 차이
- 외국인 시선의 일본 관찰

톤앤매너:

- 인간적
- 관찰형
- 조용한 몰입감
- 너무 뉴스 같지 않게
- 너무 AI 같지 않게
- B급 감성 가능
- “실제로 도쿄 사는 사람이 느끼는 감각”

---

# 목표

목표는:
“빠르게 Shorts를 반복 생산하는 시스템”

최우선:

- 빠른 제작
- 반복 가능한 구조
- 하루 3~5개 생산 가능
- 한국어 기반
- 바로 영상 제작 가능한 구조

---

# 프로젝트 구조

```txt
tokyo-insight/

  AGENTS.md
  README.md
  index.html

  data/
    2026-05-29.json

  scripts/
    generate_daily_topics.py

  assets/
    appIcon.png
```

---

# 가장 중요한 UI 구조

절대:

- 클릭 → 클릭 → 또 클릭 구조 금지

반드시:

첫 페이지(index.html)에서
날짜를 클릭하면 바로 아래에:

- 한국어 토픽
- 제목
- 후킹 문장
- 스크립트
- 썸네일 문구
- B-roll

이 한 번에 보여야 한다.

즉:
“날짜 기반 숏츠 대시보드”

형태로 제작.

---

# 데이터 규칙

모든 데이터는 반드시 한국어로 생성.

예시:

```json
{
  "date": "2026-05-29",
  "topics": [
    {
      "title": "일본은 왜 아직도 현금을 많이 쓸까?",
      "hook": "도쿄 살면서 놀란 것 중 하나.",
      "script": "...",
      "thumbnail_text": "일본은 아직 현금사회",
      "source_url": "https://example.com/article",
      "broll": ["편의점 계산", "도쿄 거리", "지하철 개찰구"]
    }
  ]
}
```

---

# 기본 대시보드에 반드시 보여야 하는 요소

각 토픽마다:

1. 제목
2. 썸네일 문구
3. 2초 후킹 문장
4. 30초 쇼츠 스크립트
5. 원문 기사 URL
6. 추천 B-roll

index.html의 빠른 제작 카드에는 위 요소를 우선 표시한다.

단, `scripts/generate_daily_topics.py`가 실시간 기사 수집으로 생성하는
`data/YYYY-MM-DD.json` 및 `posts/YYYY-MM-DD.html`에는
아래 Live Article Collection Rule의 확장 필드를 포함해야 한다.

---

# 쇼츠 스크립트 스타일

좋은 예시:

"도쿄 살면서 의외였던 게 하나 있는데요."

"일본 회사에서는 아직도 이 문화가 남아있습니다."

"한국인이 일본 와서 가장 놀라는 순간."

나쁜 예시:

"충격!! 일본에서 일어나고 있는 믿을 수 없는 일!!"

---

# 쇼츠 구조

0~2초:
강한 호기심

3~15초:
설명

15~25초:
흥미 포인트

25~35초:
짧은 마무리

---

# 메인 카테고리

1. 도쿄 라이프스타일
2. 일본 직장 문화
3. 일본 소비문화
4. 일본 AI/기술
5. 일본 일상 관찰
6. 편의점 문화
7. 조용한 문화 차이
8. 한국인이 느끼는 일본

---

# 제작 철학

완벽주의 금지.

중요한 건:

- 반복
- 속도
- 실험
- 감각 유지
- 지속 가능성

---

# Daily Workflow

1. 일본 뉴스/트렌드 수집
2. 흥미로운 토픽 선택
3. 한국어 쇼츠 스크립트 생성
4. index.html 단일 대시보드 생성
5. 첫 페이지에서 바로 확인
6. CapCut 제작
7. YouTube 업로드

---

# 토픽 수집 규칙

매일 확인:

- Yahoo Japan
- ITmedia
- Nikkei Trend
- 일본 SNS 트렌드

선정 기준:

- 30초 안에 설명 가능
- 호기심 유발
- 시각화 쉬움
- 도쿄 생활과 연결 가능
- 인간적인 관찰 느낌

피해야 할 것:

- 무거운 정치
- 복잡한 경제분석
- 의미없는 연예인 가십
- 조사 너무 오래 필요한 주제

---

# 가장 중요한 철학

“뉴스 채널”이 아니라:

도쿄 안에서 살아가는 사람이 기록하는
짧은 관찰 다큐 느낌.

그리고:
완벽보다 반복.

# Source Link Requirements

각 토픽에는 반드시 원본 기사 링크(source_url)를 포함한다.

예시:

```json id="ow2a3m"
{
  "title": "일본은 왜 아직도 현금을 많이 쓸까?",
  "hook": "도쿄 살면서 놀란 것 중 하나.",
  "script": "...",
  "thumbnail": "일본은 아직 현금사회",
  "source_url": "https://news.yahoo.co.jp/...",
  "broll": ["편의점 계산", "도쿄 거리"]
}
```

---

# HTML UI Rules

각 토픽 카드에는 반드시 아래 버튼들을 표시:

- [스크립트 보기]
- [기사 보기]

"기사 보기" 버튼 클릭 시:
해당 source_url 기사로 새 탭 이동.

---

# UX Philosophy

Tokyo Insight는 단순 아카이브가 아니라:

"빠르게 Shorts를 제작하기 위한 운영 툴"

처럼 동작해야 한다.

즉:

- 한 화면에서 빠르게 확인 가능
- 원본 기사 바로 접근 가능
- 클릭 최소화
- 제작 흐름 끊기지 않게 설계

---

# Source Handling Rules

뉴스/트렌드 수집 시:

- 반드시 원본 기사 URL 저장
- source_url 누락 금지
- 기사 링크는 HTML 카드 우측 버튼으로 표시
- 새 탭(target="\_blank")으로 열기

권장 소스:

- Yahoo Japan
- ITmedia
- Nikkei Trend
- PR Times
- 일본 SNS 트렌드

# Live Article Collection Rule

Tokyo Insight must not keep generating the same sample topics.

Every time the user runs:

```bash
python3 scripts/generate_daily_topics.py
```

the system must fetch or collect fresh articles for the current day.

## Required Behavior

The generator should:

1. Check today's date automatically.
2. Fetch current Japanese articles from real sources.
3. Use different articles each run when possible.
4. Save the fetched article metadata into:

```txt
data/YYYY-MM-DD.json
```

5. Generate a matching preview page:

```txt
posts/YYYY-MM-DD.html
```

6. Include source URLs for every selected topic.
7. Clearly separate:
   - article summary
   - original source
   - Tokyo Insight commentary angle
   - Shorts script

## Preferred Sources

Use current articles from:

- Yahoo Japan News
- ITmedia
- Nikkei XTrend
- NHK News
- PR TIMES
- Impress Watch
- Toyo Keizai
- Mainichi / Asahi / Yomiuri, when relevant

## Important Rule

Do not rely on hardcoded sample topics except as a fallback.

Hardcoded sample topics may only be used when:

- the network request fails
- no articles can be fetched
- the source format changes

If fallback topics are used, the generated HTML must clearly show:

```txt
Fallback sample data used
```

## Freshness Rules

Each run should prioritize articles published or updated within the last 24-48 hours.

If exact publication time is unavailable, prioritize:

- homepage top articles
- ranking articles
- trend sections
- latest news sections

## Deduplication Rules

Avoid repeating the same article URL already used in recent data files.

Before selecting topics, check the latest files in:

```txt
data/
```

If an article URL already appears in recent JSON files, lower its priority unless it is still a major trending story.

## Topic Selection Rules

From collected articles, select topics that are suitable for YouTube Shorts.

Prioritize articles that are:

- easy to explain in under 30 seconds
- visually easy to support with B-roll
- related to Tokyo lifestyle
- related to Japanese work culture
- related to consumer behavior
- related to AI / technology in Japan
- surprising to people outside Japan
- useful for a “living in Japan” perspective

Avoid:

- complex politics
- sensitive crime details
- celebrity gossip with no cultural insight
- medical or financial advice
- articles that require deep specialist knowledge

## Output Per Topic

Each selected topic must include:

- title
- source_name
- source_url
- published_at, if available
- article_summary
- why_it_matters
- Tokyo Insight angle
- Shorts title
- thumbnail text
- 2-second hook
- 30-second narration script
- B-roll suggestions
- editing notes
- copyright risk
- production difficulty

## Copyright Rule

Do not recommend downloading and re-uploading news videos directly.

Prefer:

- original commentary
- article screenshots with attribution
- royalty-free B-roll
- personally filmed Tokyo clips
- short reference visuals only when necessary

## HTML Preview Rule

The generated HTML preview must show:

- date
- generation time
- source list
- selected article URLs
- top 5 ranked topics
- copy-friendly script blocks
- B-roll suggestions
- copyright notes

The page should make it easy for the user to choose 3 Shorts to produce in CapCut.
