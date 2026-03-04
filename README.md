# 개인 투자 리포트 AI (RAG + MoE)

Streamlit 기반으로 만든 **개인 투자 리포트 데모 프로젝트**입니다.  
기업 관련 뉴스를 수집하고, 재무 정보를 불러온 뒤, **RAG 검색 + 간단한 MoE 조합**으로 요약 리포트를 생성합니다.  
이 프로젝트는 **RAG와 MoE 흐름을 직접 구현하며 익숙해지기 위한 데모**입니다.  
실제 서비스 수준의 정교한 분석보다, **데이터 수집 → 임베딩 → 검색 → 전문가 조합**의 전 과정을 한 번에 연결하는 데 집중했습니다.

---

## 핵심 기능

- **뉴스 수집**: Google News RSS 기반
- **재무 데이터**: `yfinance` 기반
- **RAG**: 임베딩 저장 및 코사인 유사도 검색 (MySQL 저장)
- **MoE**: 뉴스 요약 / 감성(룰 기반) / 재무 요약 / 리스크 메모 생성
- **UI**: Streamlit 단일 앱

---

## 기술 스택

- Python
- Streamlit
- SQLAlchemy + MySQL
- Sentence-Transformers
- yfinance

---

## 프로젝트 구조

- `app.py`: Streamlit UI 및 전체 흐름
- `data/`: 뉴스/재무 수집
- `rag/`: 임베딩, 저장, 검색
- `moe/`: 전문가 라우팅 및 리포트 생성
- `database/`: DB 연결/테이블 생성
- `utils/`: 설정, 텍스트 정리

---

## 실행 방법 (conda)

```bash
# 1) conda 환경 생성/활성화
conda create -n investment-demo python=3.11 -y
conda activate investment-demo

# 2) 의존성 설치
pip install -r requirements.txt

# 3) DB 테이블 생성
python database/create_tables.py

# 4) 앱 실행
streamlit run app.py
```

---

## 주의 사항

- 데모 프로젝트이며 투자 의사결정에 사용하면 안 됩니다.

---

## 앞으로 확장한다면

- LLM 기반 요약/추론 연결
- 벡터 DB(FAISS/PGVector)로 전환
- 뉴스 원문 요약 + 출처 하이라이트
- UI에서 결과 비교 및 히스토리 관리
