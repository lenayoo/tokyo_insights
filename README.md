# Tokyo Insight

Tokyo Insight는 도쿄에 사는 한국인 크리에이터가 일본 사회를 관찰형 쇼츠로 빠르게 정리하기 위한 로컬 작업 시스템입니다.

기준 문서는 `AGENTS.md`입니다.

## 구조

- `AGENTS.md`: 톤과 운영 원칙
- `data/`: 날짜별 쇼츠 주제 JSON
- `scripts/generate_daily_topics.py`: 오늘 데이터 생성 및 `index.html` 갱신
- `index.html`: 날짜 클릭 즉시 전체 주제를 보는 단일 작업 화면
- `posts/`: 날짜별 상세 미리보기 HTML
- `assets/`: 브랜딩 자산

## 사용 방법

```bash
python3 scripts/generate_daily_topics.py
```

실행하면:

1. 오늘 날짜로 일본 기사/트렌드를 수집합니다.
2. 선택된 기사 URL을 다시 열어 제목, 메타 설명, 본문 일부를 추출합니다.
3. `core_change`, `daily_life_angle`, `surprising_point`, `visual_scene`, `shorts_takeaway`를 먼저 분석합니다.
4. 분석 결과를 바탕으로 훅, 스크립트, 썸네일 문구를 생성합니다.
5. `data/YYYY-MM-DD.json`을 생성합니다.
6. `posts/YYYY-MM-DD.html` 상세 미리보기를 생성합니다.
7. 모든 날짜 데이터를 읽어서 `index.html` 단일 대시보드를 다시 만듭니다.

그다음 `index.html`을 브라우저에서 열면 됩니다.

## 분석 모드

기본 실행은 의존성 없이 동작하는 `rules` 모드입니다. 이 모드는 기사 제목, 요약, 본문 일부를 읽고 정해진 관찰 규칙으로 스크립트와 촬영 컷을 만듭니다.

기사별로 더 다르게 분석하고 싶으면 OpenAI API 키를 환경변수로 넣고 실행합니다.

```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_MODEL="gpt-4o-mini"
python3 scripts/generate_daily_topics.py
```

API 키가 있으면 각 기사마다 `openai:모델명` 분석 모드로 생성됩니다. API 키가 없거나 요청에 실패하면 자동으로 `rules` 모드로 돌아갑니다. 상세 미리보기의 `분석 포인트`에서 현재 모드를 확인할 수 있습니다.

## 모바일 확인

`index.html`과 `posts/YYYY-MM-DD.html`은 정적 파일이라 GitHub Pages, Netlify, Vercel 같은 정적 호스팅에 그대로 올릴 수 있습니다.

모바일에서는:

- 날짜 탭을 좌우로 스와이프합니다.
- 카드 안에서 `스크립트 보기`, `기사 보기`, `복사`를 바로 누릅니다.
- 버튼은 손가락 터치 기준으로 크게 잡혀 있습니다.
- 긴 기사 URL과 스크립트는 화면 밖으로 밀리지 않게 줄바꿈됩니다.

## 작업 흐름

1. 날짜를 클릭합니다.
2. 주제 제목, 훅, 스크립트, 썸네일 문구, 촬영 컷을 바로 확인합니다.
3. 카드 안에서 `스크립트 보기`, `기사 보기`, `복사`를 바로 사용합니다.
4. 바로 CapCut 작업으로 넘어갑니다.

## JSON 형식

```json
{
  "date": "2026-05-29",
  "topics": [
    {
      "title": "도쿄 편의점이 슈퍼마켓처럼 바뀌는 이유",
      "raw_article_title": "원문 기사 제목",
      "core_change": "무엇이 바뀌고 있는가",
      "daily_life_angle": "도쿄 생활자 입장에서 왜 체감되는가",
      "surprising_point": "한국인이 보면 의외인 점",
      "visual_scene": "영상으로 찍기 좋은 장면",
      "shorts_takeaway": "30초 안에 남길 한 문장",
      "hook": "도쿄에서는 편의점이 이제 장보는 곳이 되어가고 있습니다.",
      "script": "30초 내외 내레이션",
      "thumbnail_text": "편의점이 장보는 곳?",
      "source_url": "https://example.com/article",
      "broll": [
        "편의점 외관에서 입구로 들어가는 컷",
        "진열대 클로즈업"
      ]
    }
  ]
}
```

## 다음에 수정할 곳

- 새 날짜용 fallback 주제를 바꾸고 싶으면 `sample_topics()`를 수정하면 됩니다.
- 주제를 직접 편집하고 싶으면 `data/YYYY-MM-DD.json`만 수정한 뒤 스크립트를 다시 실행하면 됩니다.
- 디자인은 `scripts/generate_daily_topics.py` 안의 `page_styles()`와 `render_index_html()`에서 함께 관리합니다.
