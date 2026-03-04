import streamlit as st
from data.fetch_news import fetch_news
from data.fetch_financials import fetch_financials
from rag.embedder import embed_text
from rag.search import search_similar
from rag.store import store_embeddings
from moe.router import route_experts
from moe.agent import run_experts
from database.create_tables import create_tables

st.title("📈 개인 투자 리포트 AI (RAG + MoE)")

company = st.text_input("기업명을 입력하세요", "삼성전자")

if st.button("분석 시작"):
    create_tables()
    st.write("⏳ 데이터 수집 중...")

    news_list = fetch_news(company)
    financials = fetch_financials(company)

    st.subheader("📌 최신 뉴스 (원문)")
    st.write(news_list)

    st.write("⏳ RAG 검색 실행 중...")
    if news_list:
        news_texts = [f"{item.get('title','')} {item.get('summary','')}" for item in news_list]
        news_embs = embed_text(news_texts)
        store_embeddings(company, news_list, news_embs)
    query_emb = embed_text(company)
    retrieved = search_similar(query_emb, company)
    
    st.subheader("📌 RAG로 찾은 관련 뉴스")
    st.write(retrieved)

    st.write("⏳ MoE 분석 실행 중...")
    experts = route_experts(company, bool(financials), bool(news_list))
    report = run_experts(experts, news_list, financials, retrieved)

    st.subheader("📌 최종 투자 리포트")
    st.markdown(report)
