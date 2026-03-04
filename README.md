# 개인 투자 리포트 AI (RAG + MoE)

기업 관련 뉴스를 수집하고(RSS), 재무 정보를 불러온 뒤(yfinance), 임베딩 기반 검색과 간단한 MoE 조합으로 요약 리포트를 생성하는 데모 프로젝트입니다. Streamlit UI로 기업명/티커를 입력하면 최신 뉴스, 관련 뉴스, 요약 리포트를 확인할 수 있습니다.

## 기능 개요
- 뉴스 수집: Google News RSS 기반
- 재무 데이터: yfinance 기반
- 검색: 임베딩 저장 + 코사인 유사도 검색(MySQL 저장)
- MoE: 뉴스/재무 요약과 간단한 리스크 메모 생성
- UI: Streamlit 앱

## 프로젝트 구조
- `app.py`: Streamlit UI 및 전체 흐름
- `data/`: 뉴스/재무 수집
- `rag/`: 임베딩, 저장, 검색
- `moe/`: 전문가 라우팅 및 리포트 생성
- `database/`: DB 연결/테이블 생성
- `utils/`: 설정, 텍스트 정리

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

## 환경 변수
`.env` 파일을 프로젝트 루트에 두고 아래 값을 설정할 수 있습니다.
```
DB_USER=root
DB_PASSWORD=gkxogh11%40
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=personal
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## 주의 사항
- MySQL이 필요합니다.
- 재무 데이터는 기업명보다 티커 심볼 입력이 더 정확합니다.
  - 예: 삼성전자 -> `005930.KS`
- 이 프로젝트는 데모 목적이며 투자 의사결정에 사용하면 안 됩니다.

## 확인 방법
- `python database/create_tables.py`로 테이블 생성 여부 확인
- `streamlit run app.py`로 UI 실행 후 기업명 입력 테스트

## Skills
- Python
- Streamlit
- RAG (임베딩 저장/검색)
- MoE (간단 전문가 조합)
