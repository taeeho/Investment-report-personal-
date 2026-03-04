from moe.experts import summarize_news, summarize_financials, estimate_sentiment


def _render_section(title, body):
    return f"### {title}\n{body}\n"


def run_experts(experts, news_list, financials, retrieved):
    sections = []
    if "summary" in experts:
        sections.append(
            _render_section(
                "핵심 뉴스 요약",
                summarize_news(retrieved or news_list),
            )
        )
    if "sentiment" in experts:
        sections.append(
            _render_section(
                "시장 심리(헤드라인 기반)",
                estimate_sentiment(retrieved or news_list),
            )
        )
    if "fundamental" in experts:
        sections.append(
            _render_section(
                "재무 요약",
                summarize_financials(financials),
            )
        )
    if "risk" in experts:
        sections.append(
            _render_section(
                "리스크 메모",
                "- 모델 기반 평가가 아닌 데모용 요약입니다.\n- 추가적인 정량 분석이 필요합니다.",
            )
        )
    return "\n".join(sections).strip()
