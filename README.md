# 리뷰 감성 분석 API

고객 리뷰 텍스트를 OpenAI API로 분석하여 **감성 · 카테고리 · 한줄 요약 · 신뢰도**를 반환하는 FastAPI 서버입니다.

---

## 프로젝트 구조

```
gemini-api-server/
├── app/
│   ├── main.py            # FastAPI 앱, /analyze 엔드포인트
│   ├── gemini_client.py   # OpenAI API 연동
│   └── schemas.py         # 요청/응답 Pydantic 스키마
└── requirements.txt
```

---

## 요구 사항

| 항목 | 버전 |
|------|------|
| Python | 3.10 이상 |
| conda 환경 | `mlops` (또는 임의 환경) |
| OpenAI API Key | [platform.openai.com](https://platform.openai.com) 에서 발급 |

---

## 설치

### 1. 저장소 클론

```bash
git clone https://github.com/<your-username>/gemini-api-server.git
cd gemini-api-server
```

### 2. conda 환경 활성화

```bash
conda activate mlops
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

---

## 환경변수 설정

서버 실행 전 OpenAI API 키를 환경변수로 등록합니다.

**Linux / macOS / Git Bash (Windows)**
```bash
export OPENAI_API_KEY="sk-proj-..."
```

**Windows PowerShell**
```powershell
$env:OPENAI_API_KEY="sk-proj-..."
```

> **주의**: API 키를 코드나 Git에 커밋하지 마세요.

---

## 서버 실행

```bash
uvicorn app.main:app --reload
```

서버가 정상 시작되면 아래 주소로 접근 가능합니다.

| URL | 설명 |
|-----|------|
| http://127.0.0.1:8000/docs | Swagger UI (인터랙티브 테스트) |
| http://127.0.0.1:8000/redoc | ReDoc (API 문서) |

---

## API 사용법

### `POST /analyze`

#### 요청

```json
{
  "review_text": "배송이 너무 느려서 실망했어요. 상품 품질은 괜찮은데 포장이 엉망이었어요."
}
```

#### 응답

```json
{
  "sentiment": "부정",
  "category": "배송",
  "summary": "배송 지연 및 포장 불량에 대한 불만",
  "confidence": 0.88
}
```

#### 응답 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `sentiment` | string | 감성 분석 결과: `긍정` / `부정` / `중립` |
| `category` | string | 리뷰 카테고리: `배송` / `품질` / `가격` / `서비스` / `기타` |
| `summary` | string | 리뷰 한 줄 요약 |
| `confidence` | float | 신뢰도 (0.0 ~ 1.0) |

---

## Swagger UI 테스트 방법

1. http://127.0.0.1:8000/docs 접속
2. `POST /analyze` 클릭 → **Try it out** 버튼 클릭
3. Request body에 리뷰 텍스트 입력
4. **Execute** 클릭 → Response body에서 결과 확인

---

## 트러블슈팅

### `[Errno 2] No such file or directory` (SSL 오류)
conda 환경에서 SSL 인증서 경로가 없는 경우 발생합니다. `certifi` 패키지가 설치되어 있으면 자동으로 처리됩니다.
```bash
pip install certifi
```

### `OPENAI_API_KEY 환경변수가 설정되지 않았습니다.`
서버 실행 전 환경변수를 설정했는지 확인하세요.
```bash
echo $OPENAI_API_KEY
```

### `429 Too Many Requests`
OpenAI API 사용량 한도 초과입니다. 잠시 후 재시도하거나 [사용량 대시보드](https://platform.openai.com/usage)를 확인하세요.
