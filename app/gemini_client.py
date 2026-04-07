import json
import os

import certifi
from openai import AsyncOpenAI

# conda mlops 환경에서 SSL_CERT_FILE이 존재하지 않는 경로를 가리키는 문제 방지
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

SYSTEM_PROMPT = """당신은 고객 리뷰를 분석하는 전문가입니다.
반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 절대 포함하지 마세요.
{
  "sentiment": "긍정 또는 부정 또는 중립",
  "category": "배송 또는 품질 또는 가격 또는 서비스 또는 기타",
  "summary": "한 문장으로 요약",
  "confidence": 0.0에서 1.0 사이의 숫자
}"""


def _get_client() -> AsyncOpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
    return AsyncOpenAI(api_key=api_key)


async def analyze_review(review_text: str) -> dict:
    client = _get_client()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"리뷰: {review_text}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    raw_text = response.choices[0].message.content.strip()
    result = json.loads(raw_text)

    return {
        "sentiment": str(result.get("sentiment", "중립")),
        "category": str(result.get("category", "기타")),
        "summary": str(result.get("summary", "")),
        "confidence": float(result.get("confidence", 0.0)),
    }
