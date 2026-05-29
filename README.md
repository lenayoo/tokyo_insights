# Tokyo Insight

Tokyo Insight는 도쿄에 사는 한국인 크리에이터가 일본 사회를 관찰형 쇼츠로 빠르게 정리하기 위한 로컬 작업 시스템입니다.

기준 문서는 `AGENTS.md`입니다.

## 구조

- `AGENTS.md`: 톤과 운영 원칙
- `data/`: 날짜별 쇼츠 주제 JSON
- `scripts/generate_daily_topics.py`: 오늘 데이터 생성 및 `index.html` 갱신
- `index.html`: 날짜 클릭 즉시 전체 주제를 보는 단일 작업 화면
- `assets/`: 브랜딩 자산

별도 `posts/` 페이지는 사용하지 않습니다.

## 사용 방법

```bash
python3 scripts/generate_daily_topics.py
```

실행하면:

1. `data/YYYY-MM-DD.json`을 생성하거나 정리합니다.
2. 모든 날짜 데이터를 읽어서 `index.html` 단일 대시보드를 다시 만듭니다.

그다음 `index.html`을 브라우저에서 열면 됩니다.

## 작업 흐름

1. 날짜를 클릭합니다.
2. 주제 제목, 훅, 스크립트, 썸네일 문구, 브롤을 바로 확인합니다.
3. 카드 안에서 `스크립트 보기`, `기사 보기`, `복사`를 바로 사용합니다.
4. 바로 CapCut 작업으로 넘어갑니다.

## JSON 형식

```json
{
  "date": "2026-05-29",
  "topics": [
    {
      "title": "도쿄 편의점이 슈퍼마켓처럼 바뀌는 이유",
      "hook": "도쿄에서는 편의점이 이제 장보는 곳이 되어가고 있습니다.",
      "script": "30초 내외 내레이션",
      "thumbnail_text": "편의점이 장보는 곳?",
      "source_url": "https://example.com/article",
      "broll": [
        "편의점 외관",
        "진열대 클로즈업"
      ]
    }
  ]
}
```

## 다음에 수정할 곳

- 새 날짜용 주제를 자동으로 넣고 싶으면 `sample_topics()`를 바꾸면 됩니다.
- 주제를 직접 편집하고 싶으면 `data/YYYY-MM-DD.json`만 수정한 뒤 스크립트를 다시 실행하면 됩니다.
- 디자인은 `scripts/generate_daily_topics.py` 안의 `page_styles()`와 `render_index_html()`에서 함께 관리합니다.
