import html
import streamlit as st
from data.fetch_news import fetch_news
from data.fetch_financials import fetch_financials
from rag.embedder import embed_text
from rag.search import search_similar
from rag.store import store_embeddings
from moe.router import route_experts
from moe.agent import run_experts
from database.create_tables import create_tables
from sqlalchemy.exc import SQLAlchemyError

st.set_page_config(
    page_title="개인 투자 리포트 AI",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Space+Grotesk:wght@400;500;600&display=swap');

:root {
  --bg-1: #0f1b2b;
  --bg-2: #0c3a4a;
  --bg-3: #102035;
  --accent: #f4b860;
  --accent-2: #7fd6c2;
  --card: rgba(255, 255, 255, 0.08);
  --border: rgba(255, 255, 255, 0.12);
  --text: #eef3f7;
  --muted: #b9c3ce;
}

html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(1200px 500px at 10% 0%, #1b3553 0%, transparent 60%),
              radial-gradient(900px 400px at 90% 10%, #0f4f5c 0%, transparent 55%),
              linear-gradient(160deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
  color: var(--text);
  font-family: "Space Grotesk", sans-serif;
}

[data-testid="stSidebar"] {
  background: rgba(7, 16, 28, 0.8);
  border-right: 1px solid var(--border);
}

.hero {
  padding: 20px 24px 12px 24px;
  border: 1px solid var(--border);
  background: var(--card);
  border-radius: 16px;
  backdrop-filter: blur(8px);
}
.hero h1 {
  font-family: "Playfair Display", serif;
  font-size: 34px;
  margin: 0 0 6px 0;
}
.hero p {
  color: var(--muted);
  margin: 0;
}

.card {
  border: 1px solid var(--border);
  background: var(--card);
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}

.chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.12);
  border: 1px solid var(--border);
  color: var(--muted);
  font-size: 12px;
  margin-right: 6px;
}

.news-card {
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 10px;
}
.news-title {
  font-weight: 600;
  margin: 0 0 6px 0;
}
.news-summary {
  color: var(--muted);
  margin: 0;
  font-size: 14px;
}

.report {
  border: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.05) 100%);
  border-radius: 16px;
  padding: 18px 20px;
}

.stButton > button {
  background: linear-gradient(90deg, var(--accent) 0%, #f6d28b 100%);
  color: #1a140a;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 600;
}

[data-testid="stMetricLabel"] {
  color: #b0121b !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextInput"] [data-baseweb="input"] input,
.stTextInput > div > div > input,
.stTextInput [data-baseweb="input"] input,
[data-testid="stAppViewContainer"] input[type="text"] {
  background: rgba(255,255,255,0.08) !important;
  border: 1px solid var(--border) !important;
  color: #eef3f7 !important;
  -webkit-text-fill-color: #eef3f7 !important;
  caret-color: var(--text) !important;
  border-radius: 10px;
  text-shadow: 0 0 0 #eef3f7;
}
[data-testid="stTextInput"] input::placeholder,
.stTextInput input::placeholder {
  color: rgba(238, 243, 247, 0.55) !important;
}
</style>
    """,
    unsafe_allow_html=True,
)


def render_news(items, empty_label):
    if not items:
        st.info(empty_label)
        return

    html_blocks = []
    for item in items:
        title = html.escape(str(item.get("title", "")).strip())
        summary = html.escape(str(item.get("summary", "")).strip())
        block = (
            f'<div class="news-card">'
            f'<p class="news-title">{title or "제목 없음"}</p>'
            f'<p class="news-summary">{summary or "요약 없음"}</p>'
            f'</div>'
        )
        html_blocks.append(block)

    st.markdown("\n".join(html_blocks), unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## 설정")
    st.caption("기업명을 입력하고 리포트를 생성하세요.")
    st.markdown(
        """
<div class="card">
  <div class="chip">RAG</div>
  <div class="chip">MoE</div>
  <div class="chip">Streamlit</div>
  <p style="margin-top:10px;color:var(--muted);font-size:13px;">
    데이터 소스: RSS + yfinance
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("예시 입력")
    st.code("삼성전자\nAAPL\n005930.KS", language="text")


st.markdown(
    """
<div class="hero">
  <h1>개인 투자 리포트 AI</h1>
  <p>뉴스 수집, RAG 검색, MoE 분석을 한 번에. 입력하면 즉시 요약 리포트를 제공합니다.</p>
</div>
    """,
    unsafe_allow_html=True,
)

st.write("")

input_col, action_col = st.columns([3, 1])
with input_col:
    company = st.text_input("기업명을 입력하세요", "삼성전자")
with action_col:
    st.write("")
    run_btn = st.button("분석 시작", use_container_width=True)

st.write("")

if run_btn:
    db_ready = True
    try:
        create_tables()
    except SQLAlchemyError:
        db_ready = False
        st.error(
            "MySQL 연결에 실패했습니다. DB가 실행 중인지와 `.env` 설정을 확인하세요.",
            icon="🚨",
        )
    with st.status("데이터 수집 및 분석 중...", expanded=True) as status:
        st.write("뉴스 수집 중...")
        news_list = fetch_news(company)
        st.write("재무 데이터 수집 중...")
        financials = fetch_financials(company)

        st.write("RAG 검색 실행 중...")
        if db_ready:
            if news_list:
                news_texts = [f"{item.get('title','')} {item.get('summary','')}" for item in news_list]
                news_embs = embed_text(news_texts)
                try:
                    store_embeddings(company, news_list, news_embs)
                except SQLAlchemyError:
                    db_ready = False
                    st.warning("임베딩 저장에 실패했습니다. DB 연결을 확인하세요.", icon="⚠️")
            if db_ready:
                query_emb = embed_text(company)
                try:
                    retrieved = search_similar(query_emb, company)
                except SQLAlchemyError:
                    retrieved = []
                    db_ready = False
                    st.warning("RAG 검색에 실패했습니다. DB 연결을 확인하세요.", icon="⚠️")
            else:
                retrieved = []
        else:
            retrieved = []

        st.write("MoE 분석 실행 중...")
        experts = route_experts(company, bool(financials), bool(news_list))
        report = run_experts(experts, news_list, financials, retrieved)
        status.update(label="분석 완료", state="complete", expanded=False)

    metric_cols = st.columns(3)
    metric_cols[0].metric("수집 뉴스", len(news_list) if news_list else 0)
    metric_cols[1].metric("RAG 결과", len(retrieved) if retrieved else 0)
    metric_cols[2].metric("재무 데이터", "있음" if financials else "없음")
    if not db_ready:
        st.info("DB 미연결 상태로 RAG 기능이 비활성화되었습니다.")

    st.write("")
    tabs = st.tabs(["최신 뉴스", "RAG 관련 뉴스", "최종 리포트"])

    with tabs[0]:
        st.markdown("### 최신 뉴스 (원문)")
        render_news(news_list, "수집된 뉴스가 없습니다.")

    with tabs[1]:
        st.markdown("### RAG로 찾은 관련 뉴스")
        render_news(retrieved, "관련 뉴스가 없습니다.")

    with tabs[2]:
        st.markdown("### 최종 투자 리포트")
        st.markdown(f'<div class="report">{report}</div>', unsafe_allow_html=True)
