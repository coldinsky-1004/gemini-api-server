from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    review_text: str = Field(..., min_length=1, description="분석할 고객 리뷰 텍스트")

    model_config = {
        "json_schema_extra": {
            "example": {
                "review_text": "배송이 너무 느려서 실망했어요. 상품 품질은 괜찮은데 포장이 엉망이었어요."
            }
        }
    }


class ReviewResponse(BaseModel):
    sentiment: str = Field(..., description="감성 분석 결과 (긍정 / 부정 / 중립)")
    category: str = Field(..., description="리뷰 카테고리 (배송 / 품질 / 가격 / 서비스 / 기타)")
    summary: str = Field(..., description="한 줄 요약")
    confidence: float = Field(..., ge=0.0, le=1.0, description="신뢰도 (0.0 ~ 1.0)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "sentiment": "부정",
                "category": "배송",
                "summary": "배송 지연 및 포장 불량에 대한 불만",
                "confidence": 0.85,
            }
        }
    }
