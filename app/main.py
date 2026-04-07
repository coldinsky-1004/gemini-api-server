import json

from fastapi import FastAPI, HTTPException

from app.gemini_client import analyze_review
from app.schemas import ReviewRequest, ReviewResponse

app = FastAPI(
    title="리뷰 감성 분석 API",
    description="고객 리뷰 텍스트를 OpenAI API로 분석하여 감성, 카테고리, 요약을 반환합니다.",
    version="2.0.0",
)


@app.post("/analyze", response_model=ReviewResponse, summary="리뷰 분석")
async def analyze(request: ReviewRequest):
    """
    고객 리뷰를 분석하여 다음을 반환합니다:
    - **sentiment**: 긍정 / 부정 / 중립
    - **category**: 배송 / 품질 / 가격 / 서비스 / 기타
    - **summary**: 한 줄 요약
    - **confidence**: 신뢰도 (0.0 ~ 1.0)
    """
    try:
        result = await analyze_review(request.review_text)
        return ReviewResponse(**result)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI 응답 파싱 실패: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
