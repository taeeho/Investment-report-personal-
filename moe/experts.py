NEGATIVE_KEYWORDS = ["하락", "급락", "부진", "리콜", "소송", "경고", "위기", "감소"]
POSITIVE_KEYWORDS = ["상승", "급등", "호조", "확대", "계약", "성장", "최대"]


def summarize_news(news_list, max_items=5):
    lines = []
    for item in news_list[:max_items]:
        title = item.get("title", "")
        link = item.get("link", "")
        lines.append(f"- {title} ({link})")
    return "\n".join(lines) if lines else "- 관련 뉴스가 없습니다."


def estimate_sentiment(news_list):
    score = 0
    for item in news_list:
        title = item.get("title", "")
        if any(word in title for word in POSITIVE_KEYWORDS):
            score += 1
        if any(word in title for word in NEGATIVE_KEYWORDS):
            score -= 1
    if score > 0:
        return "뉴스 헤드라인 기준으로는 긍정 신호가 더 많습니다."
    if score < 0:
        return "뉴스 헤드라인 기준으로는 부정 신호가 더 많습니다."
    return "뉴스 헤드라인 기준으로는 중립에 가깝습니다."


def summarize_financials(financials):
    if not financials:
        return "- 재무 데이터가 없습니다."
    lines = []
    label_map = {
        "shortName": "기업명",
        "marketCap": "시가총액",
        "trailingPE": "TTM PER",
        "forwardPE": "FWD PER",
        "priceToBook": "PBR",
        "profitMargins": "순이익률",
        "revenueGrowth": "매출 성장률",
        "earningsGrowth": "이익 성장률",
        "dividendYield": "배당 수익률",
    }
    for key, label in label_map.items():
        if key in financials and financials[key] is not None:
            lines.append(f"- {label}: {financials[key]}")
    return "\n".join(lines) if lines else "- 재무 데이터가 없습니다."
