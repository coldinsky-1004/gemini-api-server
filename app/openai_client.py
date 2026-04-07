import json
import os

import certifi
from openai import AsyncOpenAI

# conda mlops 환경에서 SSL_CERT_FILE이 존재하지 않는 경로를 가리키는 문제 방지
# certifi 패키지가 제공하는 신뢰할 수 있는 CA 번들 경로로 강제 지정
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# OpenAI Chat Completions API에 전달할 시스템 프롬프트
# JSON 형식 응답을 강제하여 파싱 안정성을 높임
SYSTEM_PROMPT = """당신은 고객 리뷰를 분석하는 전문가입니다.
반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 절대 포함하지 마세요.
{
  "sentiment": "긍정 또는 부정 또는 중립",
  "category": "배송 또는 품질 또는 가격 또는 서비스 또는 기타",
  "summary": "한 문장으로 요약",
  "confidence": 0.0에서 1.0 사이의 숫자
}"""

def _get_client() -> AsyncOpenAI:
    """요청 시점에 OPENAI_API_KEY를 읽어 AsyncOpenAI 클라이언트를 생성합니다.
    모듈 로드 시 키를 검사하지 않으므로 서버 시작이 항상 가능하며,
    키가 없는 경우 API 호출 시점에 명확한 오류를 반환합니다.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
    return AsyncOpenAI(api_key=api_key)

async def analyze_review(review_text: str) -> dict:
    """리뷰 텍스트를 OpenAI API로 분석하여 감성·카테고리·요약·신뢰도를 반환합니다.
    Args:
        review_text: 분석할 고객 리뷰 원문.
    Returns:
        sentiment, category, summary, confidence 키를 포함한 dict.
    Raises:
        EnvironmentError: OPENAI_API_KEY가 설정되지 않은 경우.
        openai.OpenAIError: API 호출 실패 시.
        json.JSONDecodeError: 응답이 유효한 JSON이 아닌 경우.
    """
    client = _get_client()

    # response_format="json_object"로 지정하면 모델이 반드시 JSON만 반환
    # temperature=0.2로 낮게 설정하여 일관된 분석 결과 유도
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"리뷰: {review_text}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    # 응답 텍스트 추출 및 JSON 파싱
    raw_text = response.choices[0].message.content.strip()
    result = json.loads(raw_text)

    # 키 누락 시 기본값으로 안전하게 반환
    return {
        "sentiment": str(result.get("sentiment", "중립")),
        "category": str(result.get("category", "기타")),
        "summary": str(result.get("summary", "")),
        "confidence": float(result.get("confidence", 0.0)),
    }

