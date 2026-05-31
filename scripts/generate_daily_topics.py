#!/usr/bin/env python3
"""Collect fresh Japanese articles and build Tokyo Insight Shorts dashboards."""

from __future__ import annotations

import email.utils
import html
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
POSTS_DIR = ROOT / "posts"
INDEX_FILE = ROOT / "index.html"
MAX_TOPICS = 5
RECENT_FILE_LIMIT = 10


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    kind: str = "rss"


@dataclass
class Article:
    source_name: str
    title: str
    url: str
    summary: str = ""
    published_at: str = ""


SOURCES = [
    Source("Yahoo Japan News", "https://news.yahoo.co.jp/rss/topics/top-picks.xml"),
    Source("Yahoo Japan News IT", "https://news.yahoo.co.jp/rss/topics/it.xml"),
    Source("ITmedia NEWS", "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml"),
    Source("ITmedia Business", "https://rss.itmedia.co.jp/rss/2.0/business.xml"),
    Source("NHK News", "https://www.nhk.or.jp/rss/news/cat0.xml"),
    Source("PR TIMES", "https://prtimes.jp/", "html"),
    Source("Impress Watch", "https://www.watch.impress.co.jp/data/rss/1.0/ipw/feed.rdf"),
]


FALLBACK_SOURCE_URL = "https://news.yahoo.co.jp/"


def sample_topics() -> list[dict]:
    return [
        {
            "title": "도쿄 편의점이 슈퍼마켓처럼 바뀌는 이유",
            "source_name": "Fallback sample",
            "source_url": FALLBACK_SOURCE_URL,
            "published_at": "",
            "article_summary": "실시간 기사 수집에 실패했을 때 쓰는 예비 샘플입니다.",
            "why_it_matters": "도쿄 생활 리듬과 1인 가구 소비를 쉽게 보여줄 수 있습니다.",
            "tokyo_insight_angle": "편의점 진열대 변화로 도쿄 사람들의 생활 동선을 관찰합니다.",
            "shorts_title": "도쿄 편의점이 슈퍼마켓처럼 바뀌는 이유",
            "thumbnail_text": "편의점이 장보는 곳?",
            "hook": "도쿄에서는 편의점이 이제 장보는 곳이 되어가고 있습니다.",
            "script": (
                "도쿄에 살면서 요즘 가장 현실적으로 느끼는 변화 중 하나는 편의점의 역할입니다. "
                "예전에는 급할 때 들르는 곳이었다면, 지금은 작은 슈퍼처럼 일상 장보기를 대신하는 분위기가 더 강해졌습니다. "
                "1인 가구가 많고, 멀리 큰 마트까지 가기엔 시간이 애매한 도시에서는 이런 변화가 자연스럽습니다. "
                "일본의 변화는 대개 조용하게 오는데, 편의점 진열대가 바뀌는 방식은 지금 도쿄의 생활 리듬을 꽤 정확하게 보여줍니다."
            ),
            "broll": ["주택가 편의점 외관", "반찬류 진열대", "작은 장바구니", "역 앞 상점가"],
            "editing_notes": "직접 촬영한 편의점 외관과 손 클로즈업 위주로 빠르게 구성.",
            "copyright_risk": "뉴스 영상 재업로드 금지. 기사 화면은 짧게 출처 표시용으로만 사용.",
            "production_difficulty": "쉬움",
        },
        {
            "title": "일본 회사에서 AI가 먼저 바꾸는 것은 회의보다 문서다",
            "source_name": "Fallback sample",
            "source_url": FALLBACK_SOURCE_URL,
            "published_at": "",
            "article_summary": "실시간 기사 수집에 실패했을 때 쓰는 예비 샘플입니다.",
            "why_it_matters": "일본의 AI 도입은 화려한 제품보다 업무 흐름에서 먼저 체감됩니다.",
            "tokyo_insight_angle": "도쿄 오피스 문화 안쪽에서 조용히 바뀌는 문서 업무를 봅니다.",
            "shorts_title": "일본 회사에서 AI가 먼저 바꾸는 것은 회의보다 문서다",
            "thumbnail_text": "일본 회사도 AI 문서",
            "hook": "일본의 AI 변화는 생각보다 조용한 곳에서 시작되고 있습니다.",
            "script": (
                "일본에서 AI 이야기를 들으면 로봇이나 신기한 기계를 떠올리기 쉽지만, 실제 변화는 더 조용합니다. "
                "회의록, 문서 초안, 사내 자료 정리처럼 눈에 잘 안 보이는 업무부터 바뀌고 있습니다. "
                "도쿄 회사 문화에서 흥미로운 건, 새로운 기술도 갑자기 생활을 뒤집기보다 기존 절차 안으로 천천히 들어온다는 점입니다. "
                "그래서 일본의 AI 전환은 멋진 데모보다 매일 쓰는 문서에서 먼저 느껴질 가능성이 큽니다."
            ),
            "broll": ["오피스 빌딩", "노트북 타이핑", "회의실 문", "문서 위 커서"],
            "editing_notes": "오피스 출근길, 키보드, 문서 화면 대체 컷으로 구성.",
            "copyright_risk": "제품 화면이나 기사 이미지는 짧게 참고만 사용.",
            "production_difficulty": "쉬움",
        },
    ]


def ensure_directories() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    POSTS_DIR.mkdir(exist_ok=True)


def clean_text(value: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", text).strip()


def fetch_url(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "TokyoInsightBot/1.0 (+https://example.local)",
            "Accept": "application/rss+xml, application/xml, text/xml, text/html;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            return response.read()
    except urllib.error.URLError as error:
        reason = getattr(error, "reason", None)
        if isinstance(reason, ssl.SSLCertVerificationError):
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(request, timeout=12, context=context) as response:
                return response.read()
        raise


def parse_date(value: str) -> str:
    if not value:
        return ""
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo:
            parsed = parsed.astimezone(timezone.utc)
        return parsed.isoformat()
    except (TypeError, ValueError, IndexError):
        return clean_text(value)


def child_text(element: ET.Element, names: tuple[str, ...]) -> str:
    for child in list(element):
        local_name = child.tag.rsplit("}", 1)[-1].lower()
        if local_name in names:
            return clean_text(child.text or "")
    return ""


def child_link(element: ET.Element) -> str:
    for child in list(element):
        local_name = child.tag.rsplit("}", 1)[-1].lower()
        if local_name == "link":
            href = child.attrib.get("href")
            return clean_text(href or child.text or "")
    return ""


def parse_feed(source: Source, content: bytes) -> list[Article]:
    root = ET.fromstring(content)
    items = [
        element
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1].lower() in {"item", "entry"}
    ]
    articles = []
    for item in items[:30]:
        title = child_text(item, ("title",))
        url = child_link(item)
        summary = child_text(item, ("description", "summary", "content", "encoded"))
        published_at = child_text(item, ("pubdate", "published", "updated", "date", "dc:date"))
        if title and url:
            articles.append(
                Article(
                    source_name=source.name,
                    title=title,
                    url=normalize_url(url),
                    summary=summary,
                    published_at=parse_date(published_at),
                )
            )
    return articles


def parse_html_links(source: Source, content: bytes) -> list[Article]:
    text = content.decode("utf-8", errors="ignore")
    articles = []
    seen: set[str] = set()
    for match in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', text, re.I | re.S):
        href, label = match.groups()
        title = clean_text(label)
        if len(title) < 12:
            continue
        url = urllib.parse.urljoin(source.url, html.unescape(href))
        parsed = urllib.parse.urlsplit(url)
        if parsed.netloc and "prtimes.jp" not in parsed.netloc:
            continue
        if "/main/html/" not in parsed.path and "/main/html/rd/" not in parsed.path:
            continue
        normalized = normalize_url(url)
        if normalized in seen:
            continue
        seen.add(normalized)
        articles.append(Article(source.name, title, normalized))
        if len(articles) >= 30:
            break
    return articles


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(clean_text(url))
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered_query = [
        (key, value)
        for key, value in query
        if not key.lower().startswith("utm_") and key.lower() not in {"fbclid", "gclid"}
    ]
    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path.rstrip("/") or parsed.path,
            urllib.parse.urlencode(filtered_query),
            "",
        )
    )


def collect_articles() -> tuple[list[Article], list[str]]:
    articles: list[Article] = []
    errors: list[str] = []
    seen: set[str] = set()
    for source in SOURCES:
        try:
            content = fetch_url(source.url)
            parsed_articles = parse_html_links(source, content) if source.kind == "html" else parse_feed(source, content)
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ValueError) as error:
            errors.append(f"{source.name}: {error}")
            continue
        for article in parsed_articles:
            if article.url in seen:
                continue
            seen.add(article.url)
            articles.append(article)
        time.sleep(0.2)
    return articles, errors


def load_recent_urls() -> set[str]:
    urls: set[str] = set()
    paths = sorted(DATA_DIR.glob("*.json"), reverse=True)[:RECENT_FILE_LIMIT]
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for topic in payload.get("topics", []):
            source_url = topic.get("source_url")
            if source_url:
                urls.add(normalize_url(str(source_url)))
    return urls


KEYWORD_RULES = [
    (("ai", "生成ai", "chatgpt", "人工知能", "ロボット", "半導体", "アプリ", "スマホ"), "일본 AI/기술"),
    (("コンビニ", "セブン", "ローソン", "ファミマ", "スーパー", "小売", "食品"), "편의점 문화"),
    (("会社", "働", "賃上げ", "転職", "出社", "リモート", "人手不足"), "일본 직장 문화"),
    (("東京", "渋谷", "新宿", "駅", "電車", "地下鉄", "街", "観光"), "도쿄 라이프스타일"),
    (("値上げ", "節約", "消費", "物価", "売れ", "購入", "サービス"), "일본 소비문화"),
]


def classify_article(article: Article) -> str:
    haystack = f"{article.title} {article.summary}".lower()
    for keywords, category in KEYWORD_RULES:
        if any(keyword.lower() in haystack for keyword in keywords):
            return category
    return "일본 일상 관찰"


def score_article(article: Article, recent_urls: set[str]) -> int:
    haystack = f"{article.title} {article.summary}".lower()
    score = 0
    for keywords, _category in KEYWORD_RULES:
        score += sum(12 for keyword in keywords if keyword.lower() in haystack)
    if any(word in article.source_name.lower() for word in ("itmedia", "impress", "pr times")):
        score += 8
    if "tokyo" in haystack or "東京" in haystack:
        score += 14
    if article.published_at:
        score += 4
    if normalize_url(article.url) in recent_urls:
        score -= 80
    if any(blocked in haystack for blocked in ("殺人", "逮捕", "容疑", "事故", "政党", "選挙", "火葬", "訃報")):
        score -= 35
    return score


def topic_focus(article: Article, category: str) -> str:
    haystack = f"{article.title} {article.summary}"
    rules = [
        (("本社", "移転"), "도쿄 본사 집중이 조금씩 흔들리는 흐름"),
        (("居酒屋", "倒産"), "일본 이자카야가 버티기 어려워지는 배경"),
        (("ドンキ", "ご当地", "ドンペン"), "돈키호테가 지역 한정 캐릭터로 소비자를 붙잡는 방식"),
        (("copilot", "microsoft 365"), "오피스 업무 안으로 AI 비서가 들어오는 방식"),
        (("コンビニ", "スーパー"), "편의점이 생활 인프라처럼 넓어지는 흐름"),
        (("値上げ", "物価"), "가격 변화가 일본인의 일상 선택을 바꾸는 흐름"),
        (("リモート", "出社", "働"), "일본 회사의 일하는 방식이 조용히 바뀌는 흐름"),
        (("スマホ", "アプリ"), "스마트폰 서비스가 일본 생활 동선을 바꾸는 흐름"),
    ]
    lower_haystack = haystack.lower()
    for keywords, focus in rules:
        if all(keyword.lower() in lower_haystack for keyword in keywords[:2]):
            return focus
        if any(keyword.lower() in lower_haystack for keyword in keywords):
            return focus
    fallback = {
        "일본 AI/기술": "일본 기술이 일상 업무 안으로 조용히 들어오는 흐름",
        "편의점 문화": "편의점과 가까운 소비가 생활 리듬을 바꾸는 흐름",
        "일본 직장 문화": "일본 회사 문화가 천천히 재조정되는 흐름",
        "도쿄 라이프스타일": "도쿄 생활의 기준이 조금씩 바뀌는 흐름",
        "일본 소비문화": "일본 소비자가 덜 피곤한 선택을 찾는 흐름",
        "일본 일상 관찰": "일본 일상에서 보이는 작은 변화",
    }
    return fallback.get(category, "일본 일상에서 보이는 작은 변화")


def korean_topic_title(article: Article, category: str) -> str:
    focus = topic_focus(article, category)
    if focus != "일본 일상에서 보이는 작은 변화":
        return focus
    templates = {
        "일본 AI/기술": "일본 기술 기사에서 보이는 조용한 AI 변화",
        "편의점 문화": "일본 편의점 기사에서 보이는 생활 변화",
        "일본 직장 문화": "일본 직장 문화가 조금씩 바뀌는 신호",
        "도쿄 라이프스타일": "도쿄 생활 기사에서 보이는 도시의 작은 변화",
        "일본 소비문화": "일본 소비 기사에서 보이는 요즘 사람들의 선택",
        "일본 일상 관찰": "일본 뉴스에서 보이는 일상의 작은 변화",
    }
    return templates.get(category, "일본 뉴스에서 보이는 일상의 작은 변화")


def broll_for_category(category: str) -> list[str]:
    mapping = {
        "일본 AI/기술": ["노트북 타이핑 클로즈업", "도쿄 오피스 빌딩", "스마트폰 화면 손동작", "역 안 디지털 광고판"],
        "편의점 문화": ["편의점 외관", "계산대 손 클로즈업", "도시락 진열대", "퇴근길 골목 워킹샷"],
        "일본 직장 문화": ["아침 출근길 역 인파", "사무실 빌딩 입구", "회의실 문패", "노트북을 덮는 손"],
        "도쿄 라이프스타일": ["도쿄 역 앞 거리", "전철 개찰구", "주택가 골목", "신호등 앞 사람들"],
        "일본 소비문화": ["매장 진열대", "가격표 클로즈업", "쇼핑백을 든 손", "번화가 워킹샷"],
        "일본 일상 관찰": ["도쿄 거리 스냅", "전철 내부 손잡이", "작은 상점 외관", "횡단보도 와이드샷"],
    }
    return mapping.get(category, mapping["일본 일상 관찰"])


def script_for_article(article: Article, category: str) -> tuple[str, str, str, str, str, str]:
    source = article.source_name
    focus = topic_focus(article, category)
    title = korean_topic_title(article, category)
    thumbnail = {
        "일본 AI/기술": "일본 AI는 조용하다",
        "편의점 문화": "편의점이 바뀌는 중",
        "일본 직장 문화": "일본 회사의 변화",
        "도쿄 라이프스타일": "도쿄 생활의 신호",
        "일본 소비문화": "요즘 일본 소비",
        "일본 일상 관찰": "일본 일상의 변화",
    }.get(category, "일본 일상의 변화")
    hook = {
        "일본 AI/기술": "일본의 기술 변화는 생각보다 조용한 곳에서 먼저 보입니다.",
        "편의점 문화": "도쿄 살면서 편의점 변화를 보면 생활 리듬이 보입니다.",
        "일본 직장 문화": "일본 회사 문화도 아주 천천히 달라지고 있습니다.",
        "도쿄 라이프스타일": "도쿄 생활에서 이런 작은 변화가 은근히 크게 느껴집니다.",
        "일본 소비문화": "요즘 일본 소비는 가격보다 피로감이 더 중요해 보입니다.",
        "일본 일상 관찰": "일본 뉴스에서 가끔 생활감 있는 변화가 딱 보일 때가 있습니다.",
    }.get(category, "일본 뉴스에서 생활감 있는 변화가 보일 때가 있습니다.")
    article_summary = (
        f"{source}에서 다룬 최근 기사입니다. 핵심은 {focus}이 일본 사회와 생활 현장에서 주목받고 있다는 점입니다."
    )
    why_it_matters = (
        f"이 주제는 {category} 관점으로 30초 안에 설명하기 쉽고, 도쿄의 거리와 일상 장면으로 바로 시각화할 수 있습니다."
    )
    angle = (
        "뉴스 자체를 크게 해설하기보다, 도쿄에 사는 사람이 실제 생활에서 어떤 장면으로 이 변화를 느낄 수 있는지에 초점을 둡니다."
    )
    script = (
        f"도쿄 살면서 일본 뉴스를 볼 때 흥미로운 건, 큰 변화가 항상 크게 등장하지는 않는다는 점입니다. "
        f"이번에 {source}에서 다룬 이슈도 그렇습니다. 겉으로는 하나의 기사처럼 보이지만, 실제로는 {category}의 흐름을 보여주는 작은 신호에 가깝습니다. "
        "도쿄에서는 이런 변화가 역, 편의점, 회사, 매장 같은 평범한 장소에서 먼저 느껴집니다. "
        "그래서 이 주제는 거창한 뉴스라기보다, 일본 생활의 결이 조금 바뀌고 있다는 관찰로 보는 게 더 자연스럽습니다."
    )
    return title, thumbnail, hook, article_summary, why_it_matters, angle, script


def build_topic(article: Article, rank: int) -> dict:
    category = classify_article(article)
    title, thumbnail, hook, article_summary, why_it_matters, angle, script = script_for_article(article, category)
    return {
        "rank": rank,
        "title": title,
        "source_name": article.source_name,
        "source_url": article.url,
        "published_at": article.published_at,
        "article_summary": article_summary,
        "why_it_matters": why_it_matters,
        "tokyo_insight_angle": angle,
        "shorts_title": title,
        "thumbnail_text": thumbnail,
        "hook": hook,
        "script": script,
        "broll": broll_for_category(category),
        "editing_notes": "직접 촬영한 도쿄 거리, 손동작, 매장 외관 중심으로 구성하고 기사 화면은 출처 확인용으로 짧게만 사용.",
        "copyright_risk": "뉴스 영상이나 사진을 그대로 재업로드하지 말고, 원문 링크와 출처를 표시한 뒤 자체 내레이션과 직접 촬영 B-roll을 사용.",
        "production_difficulty": "쉬움",
    }


def build_payload(target_date: str) -> dict:
    recent_urls = load_recent_urls()
    articles, errors = collect_articles()
    ranked = sorted(articles, key=lambda article: score_article(article, recent_urls), reverse=True)
    selected: list[Article] = []
    source_counts: dict[str, int] = {}
    for article in ranked:
        if normalize_url(article.url) in recent_urls:
            continue
        if score_article(article, recent_urls) < -10:
            continue
        if source_counts.get(article.source_name, 0) >= 2:
            continue
        selected.append(article)
        source_counts[article.source_name] = source_counts.get(article.source_name, 0) + 1
        if len(selected) >= MAX_TOPICS:
            break
    if len(selected) < MAX_TOPICS:
        for article in ranked:
            if article in selected or normalize_url(article.url) in recent_urls:
                continue
            if score_article(article, recent_urls) < -10:
                continue
            selected.append(article)
            if len(selected) >= MAX_TOPICS:
                break
    fallback_used = len(selected) == 0
    topics = sample_topics() if fallback_used else [build_topic(article, index) for index, article in enumerate(selected, 1)]
    return {
        "date": target_date,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "fallback_used": fallback_used,
        "source_list": [source.name for source in SOURCES],
        "collection_errors": errors,
        "topics": topics,
    }


def normalize_topic(topic: dict) -> dict:
    broll = topic.get("broll") or topic.get("broll_suggestions") or []
    script = topic.get("script") or topic.get("30_second_script") or topic.get("narration_script") or ""
    source_url = topic.get("source_url", "")
    if not source_url and topic.get("source_links"):
        first_link = topic["source_links"][0]
        if isinstance(first_link, dict):
            source_url = first_link.get("url", "")
    title = str(topic.get("shorts_title") or topic.get("title") or "").strip()
    return {
        "rank": int(topic.get("rank", 0) or 0),
        "title": title,
        "source_name": str(topic.get("source_name", "")).strip(),
        "source_url": str(source_url).strip(),
        "published_at": str(topic.get("published_at", "")).strip(),
        "article_summary": str(topic.get("article_summary", "")).strip(),
        "why_it_matters": str(topic.get("why_it_matters", "")).strip(),
        "tokyo_insight_angle": str(topic.get("tokyo_insight_angle", topic.get("Tokyo Insight angle", ""))).strip(),
        "shorts_title": title,
        "thumbnail_text": str(topic.get("thumbnail_text", topic.get("thumbnail", ""))).strip(),
        "hook": str(topic.get("hook", "")).strip(),
        "script": str(script).strip(),
        "broll": [str(item).strip() for item in broll if str(item).strip()],
        "editing_notes": str(topic.get("editing_notes", "")).strip(),
        "copyright_risk": str(topic.get("copyright_risk", "")).strip(),
        "production_difficulty": str(topic.get("production_difficulty", "")).strip(),
    }


def normalize_payload(payload: dict, target_date: str) -> dict:
    topics = [normalize_topic(topic) for topic in payload.get("topics", [])]
    topics = [topic for topic in topics if topic["title"] and topic["source_url"]]
    return {
        "date": str(payload.get("date", target_date)),
        "generated_at": str(payload.get("generated_at", "")),
        "fallback_used": bool(payload.get("fallback_used", False)),
        "source_list": list(payload.get("source_list", [])),
        "collection_errors": list(payload.get("collection_errors", [])),
        "topics": topics,
    }


def load_archives() -> list[dict]:
    archives = []
    for path in sorted(DATA_DIR.glob("*.json"), reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
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
      --bg: #f6f3ee;
      --paper: rgba(255, 255, 255, 0.94);
      --paper-strong: #fff;
      --ink: #202528;
      --muted: #68747b;
      --line: rgba(32, 37, 40, 0.12);
      --accent: #c04f36;
      --accent-soft: rgba(192, 79, 54, 0.12);
      --good: #28745b;
      --warn: #9b5a17;
      --shadow: 0 14px 34px rgba(35, 31, 28, 0.08);
      --radius: 8px;
      --max: 1120px;
      --sans: "Hiragino Sans", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif;
    }
    * { box-sizing: border-box; }
    html { background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.6; scroll-behavior: smooth; text-size-adjust: 100%; }
    body { margin: 0; min-height: 100vh; overflow-x: hidden; }
    button, textarea { font: inherit; }
    .shell { width: min(calc(100% - 24px), var(--max)); margin: 0 auto; padding: calc(20px + env(safe-area-inset-top)) 0 calc(48px + env(safe-area-inset-bottom)); }
    .topbar, .date-rail, .day-panel, .topic-card, .block { background: var(--paper); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); }
    .topbar { padding: 22px; margin-bottom: 14px; }
    .eyebrow { margin: 0 0 8px; color: var(--accent); font-size: .74rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    h1, h2, h3 { margin: 0; line-height: 1.24; letter-spacing: 0; }
    h1 { font-size: 2.8rem; margin-bottom: 10px; }
    h2 { font-size: 1.8rem; }
    h3 { font-size: 1.08rem; }
    p { margin: 0; }
    a { color: inherit; overflow-wrap: anywhere; }
    .lead, .small, .day-meta, .source-line { color: var(--muted); }
    .lead { max-width: 66ch; }
    .date-rail { position: sticky; top: 10px; z-index: 5; padding: 12px; margin-bottom: 14px; }
    .date-scroll { display: flex; gap: 8px; overflow-x: auto; overscroll-behavior-x: contain; padding-bottom: 2px; scrollbar-width: none; }
    .date-scroll::-webkit-scrollbar { display: none; }
    .day-actions, .script-toolbar, .source-list { display: flex; gap: 8px; flex-wrap: wrap; }
    .date-tab, .ghost-button, .tool-button, .copy-button { min-height: 44px; display: inline-flex; align-items: center; justify-content: center; border: 1px solid var(--line); border-radius: 999px; padding: 9px 14px; background: var(--paper-strong); color: var(--ink); cursor: pointer; text-decoration: none; -webkit-tap-highlight-color: transparent; }
    .date-tab { flex-direction: column; align-items: flex-start; min-width: 102px; }
    .date-tab.is-active, .copy-button { background: var(--accent-soft); border-color: rgba(192, 79, 54, .24); color: var(--accent); }
    .date-tab span { font-size: .78rem; color: var(--muted); }
    .day-panel { padding: 20px; }
    .day-panel[hidden] { display: none; }
    .day-header { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 12px; margin-bottom: 16px; }
    .day-header > div:first-child { min-width: 0; }
    .topic-list { display: grid; gap: 14px; }
    .topic-card { padding: 18px; }
    .topic-head { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 12px; min-width: 0; }
    .topic-number { flex: 0 0 auto; width: 32px; height: 32px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; background: var(--accent-soft); color: var(--accent); font-weight: 700; }
    .topic-head > div { min-width: 0; }
    .hook { margin-top: 10px; padding: 12px 14px; border-left: 3px solid var(--accent); border-radius: 0 var(--radius) var(--radius) 0; background: var(--accent-soft); }
    .topic-grid { display: grid; grid-template-columns: 1fr; gap: 12px; margin-top: 14px; }
    .block { padding: 14px; box-shadow: none; background: rgba(255, 255, 255, .66); }
    .label { display: inline-block; margin-bottom: 8px; color: var(--accent); font-size: .74rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .thumbnail-chip, .badge { display: inline-flex; align-items: center; padding: 7px 10px; border-radius: 999px; background: var(--accent-soft); color: var(--accent); font-weight: 700; }
    .badge.live { color: var(--good); background: rgba(40, 116, 91, .12); }
    .badge.fallback { color: var(--warn); background: rgba(155, 90, 23, .13); }
    .script-wrap { display: grid; gap: 10px; }
    .script-box { width: 100%; min-height: 150px; resize: vertical; padding: 14px; border: 1px solid var(--line); border-radius: var(--radius); background: rgba(255, 255, 255, .9); color: var(--ink); line-height: 1.65; }
    ul { margin: 0; padding-left: 18px; }
    li + li { margin-top: 6px; }
    .empty { padding: 28px; text-align: center; color: var(--muted); }
    @media (min-width: 760px) { .topic-grid.two-col { grid-template-columns: minmax(0, 1.15fr) minmax(300px, .85fr); } }
    @media (max-width: 760px) {
      h1 { font-size: 2rem; }
      h2 { font-size: 1.42rem; }
      .shell { width: min(calc(100% - 16px), var(--max)); padding-top: calc(10px + env(safe-area-inset-top)); }
      .topbar, .date-rail, .day-panel, .topic-card { padding: 14px; }
      .topbar { margin-bottom: 10px; }
      .lead { font-size: .95rem; }
      .date-rail { top: 0; margin-left: -8px; margin-right: -8px; border-radius: 0; border-left: 0; border-right: 0; }
      .date-tab { min-width: 84px; padding: 8px 12px; }
      .day-header { display: grid; align-items: stretch; }
      .day-actions, .script-toolbar { display: grid; grid-template-columns: 1fr 1fr; }
      .script-toolbar .copy-button { grid-column: 1 / -1; }
      .ghost-button, .tool-button, .copy-button { width: 100%; padding-left: 10px; padding-right: 10px; }
      .topic-card { box-shadow: 0 8px 22px rgba(35, 31, 28, .07); }
      .topic-head { gap: 10px; }
      .topic-number { width: 28px; height: 28px; font-size: .88rem; }
      .hook { padding: 10px 12px; }
      .block { padding: 12px; }
      .script-box { min-height: 190px; font-size: 1rem; }
    }
    @media (max-width: 420px) {
      h1 { font-size: 1.72rem; }
      h2 { font-size: 1.24rem; }
      h3 { font-size: 1rem; }
      .day-actions, .script-toolbar { grid-template-columns: 1fr; }
      .script-toolbar .copy-button { grid-column: auto; }
      .badge { width: 100%; justify-content: center; margin-bottom: 6px; }
      .thumbnail-chip { max-width: 100%; white-space: normal; }
      .topic-grid { gap: 10px; margin-top: 10px; }
    }
    """


def render_list(items: list[str]) -> str:
    entries = "\n".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul>{entries}</ul>"


def render_topic(topic: dict, topic_index: int, day_index: int, detailed: bool = False) -> str:
    script_id = f"script-{day_index}-{topic_index}"
    source_url = html.escape(topic["source_url"])
    detail_blocks = ""
    if detailed:
        detail_blocks = f"""
              <section class="block">
                <span class="label">기사 요약</span>
                <p>{html.escape(topic["article_summary"])}</p>
              </section>
              <section class="block">
                <span class="label">Tokyo Insight Angle</span>
                <p>{html.escape(topic["tokyo_insight_angle"])}</p>
              </section>
              <section class="block">
                <span class="label">저작권 메모</span>
                <p>{html.escape(topic["copyright_risk"])}</p>
              </section>
        """
    return f"""
        <article class="topic-card">
          <div class="topic-head">
            <span class="topic-number">{topic_index}</span>
            <div>
              <h3>{html.escape(topic["title"])}</h3>
              <p class="source-line">{html.escape(topic["source_name"])} · <a href="{source_url}" target="_blank" rel="noreferrer noopener">원문 기사</a></p>
              <p class="hook">{html.escape(topic["hook"])}</p>
            </div>
          </div>
          <div class="topic-grid two-col">
            <section class="block">
              <span class="label">스크립트</span>
              <div class="script-wrap">
                <div class="script-toolbar">
                  <button class="tool-button" type="button" data-focus-target="{script_id}">스크립트 보기</button>
                  <a class="tool-button" href="{source_url}" target="_blank" rel="noreferrer noopener">기사 보기</a>
                  <button class="copy-button" type="button" data-copy-target="{script_id}">복사</button>
                </div>
                <textarea class="script-box" id="{script_id}" readonly spellcheck="false" onclick="this.focus();this.select();">{html.escape(topic["script"])}</textarea>
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
              {detail_blocks}
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
    badge = "Fallback sample data used" if payload.get("fallback_used") else "Live articles collected"
    badge_class = "fallback" if payload.get("fallback_used") else "live"
    return f"""
      <section class="day-panel" id="{panel_id}"{hidden_attr}>
        <div class="day-header">
          <div>
            <p class="eyebrow">Daily Shorts Board</p>
            <h2>{html.escape(korean_date(payload["date"]))}</h2>
            <p class="day-meta"><span class="badge {badge_class}">{html.escape(badge)}</span> {len(payload["topics"])}개 주제. 도쿄에서 바로 찍고 바로 쓰기 좋게 정리했습니다.</p>
          </div>
          <div class="day-actions">
            <button class="ghost-button" type="button" data-copy-bundle-target="{bundle_id}">하루 스크립트 복사</button>
            <a class="ghost-button" href="posts/{html.escape(payload['date'])}.html">상세 미리보기</a>
          </div>
        </div>
        <textarea id="{bundle_id}" hidden>{html.escape(bundle)}</textarea>
        <div class="topic-list">{topics_html}</div>
      </section>
    """


def scripts_js() -> str:
    return """
      const tabs = Array.from(document.querySelectorAll(".date-tab"));
      const panels = Array.from(document.querySelectorAll(".day-panel[id]"));
      function activatePanel(targetId) {
        tabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.target === targetId));
        panels.forEach((panel) => { panel.hidden = panel.id !== targetId; });
        const activePanel = document.getElementById(targetId);
        if (activePanel) activePanel.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      tabs.forEach((tab) => tab.addEventListener("click", () => activatePanel(tab.dataset.target)));
      async function copyText(text) {
        try { await navigator.clipboard.writeText(text); return true; }
        catch (error) {
          const helper = document.createElement("textarea");
          helper.value = text; document.body.appendChild(helper); helper.select();
          const copied = document.execCommand("copy"); document.body.removeChild(helper); return copied;
        }
      }
      document.querySelectorAll("[data-copy-target]").forEach((button) => {
        button.addEventListener("click", async () => {
          const field = document.getElementById(button.dataset.copyTarget);
          if (!field || !(await copyText(field.value))) return;
          const original = button.textContent; button.textContent = "복사됨";
          window.setTimeout(() => { button.textContent = original; }, 1200);
        });
      });
      document.querySelectorAll("[data-focus-target]").forEach((button) => {
        button.addEventListener("click", () => {
          const field = document.getElementById(button.dataset.focusTarget);
          if (!field) return; field.scrollIntoView({ behavior: "smooth", block: "center" }); field.focus(); field.select();
        });
      });
      document.querySelectorAll("[data-copy-bundle-target]").forEach((button) => {
        button.addEventListener("click", async () => {
          const field = document.getElementById(button.dataset.copyBundleTarget);
          if (!field || !(await copyText(field.value))) return;
          const original = button.textContent; button.textContent = "하루분 복사됨";
          window.setTimeout(() => { button.textContent = original; }, 1200);
        });
      });
    """


def render_index_html(archives: list[dict]) -> str:
    if not archives:
        day_panels = '<section class="day-panel"><div class="empty">아직 생성된 날짜가 없습니다.</div></section>'
        date_tabs = ""
    else:
        day_panels = "\n".join(render_day_panel(payload, day_index, day_index == 0) for day_index, payload in enumerate(archives))
        date_tabs = "\n".join(
            f"""<button class="date-tab{' is-active' if day_index == 0 else ''}" type="button" data-target="day-{payload['date']}"><strong>{html.escape(chip_date(payload["date"]))}</strong><span>{len(payload["topics"])}개 주제</span></button>"""
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
        <p class="lead">날짜를 누르면 바로 훅, 스크립트, 썸네일 문구, 브롤이 펼쳐집니다. 뉴스보다 관찰에 가깝고, 완성도보다 반복 가능한 생산 속도에 맞췄습니다.</p>
      </header>
      <section class="date-rail"><div class="date-scroll">{date_tabs}</div></section>
      {day_panels}
    </main>
    <script>{scripts_js()}</script>
  </body>
</html>
"""


def render_post_html(payload: dict) -> str:
    topics_html = "\n".join(render_topic(topic, index, 0, detailed=True) for index, topic in enumerate(payload["topics"], start=1))
    source_list = render_list(payload.get("source_list", []))
    selected_urls = render_list([f"{topic['source_name']}: {topic['source_url']}" for topic in payload["topics"]])
    badge = "Fallback sample data used" if payload.get("fallback_used") else "Live articles collected"
    badge_class = "fallback" if payload.get("fallback_used") else "live"
    errors = payload.get("collection_errors") or []
    error_html = f"<section class=\"block\"><span class=\"label\">수집 메모</span>{render_list(errors)}</section>" if errors else ""
    return f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tokyo Insight {html.escape(payload['date'])}</title>
    <style>{page_styles()}</style>
  </head>
  <body>
    <main class="shell">
      <header class="topbar">
        <p class="eyebrow">Tokyo Insight Preview</p>
        <h1>{html.escape(korean_date(payload["date"]))} 숏츠 후보</h1>
        <p class="lead"><span class="badge {badge_class}">{html.escape(badge)}</span> 생성 시각: {html.escape(payload.get("generated_at", ""))}</p>
      </header>
      <section class="day-panel">
        <div class="topic-grid two-col">
          <section class="block"><span class="label">확인한 소스</span>{source_list}</section>
          <section class="block"><span class="label">선택된 기사 URL</span>{selected_urls}</section>
        </div>
        {error_html}
      </section>
      <section class="topic-list">{topics_html}</section>
    </main>
    <script>{scripts_js()}</script>
  </body>
</html>
"""


def write_json_file(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_directories()
    target_date = date.today().isoformat()
    json_path = DATA_DIR / f"{target_date}.json"
    post_path = POSTS_DIR / f"{target_date}.html"

    payload = normalize_payload(build_payload(target_date), target_date)
    write_json_file(json_path, payload)
    write_text_file(post_path, render_post_html(payload))

    archives = load_archives()
    write_text_file(INDEX_FILE, render_index_html(archives))

    mode = "fallback" if payload.get("fallback_used") else "live"
    print(f"생성 완료: {json_path.relative_to(ROOT)} ({mode})")
    print(f"생성 완료: {post_path.relative_to(ROOT)}")
    print(f"갱신 완료: {INDEX_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
