from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    """POST /analyze 요청 스키마.
    Attributes:
        review_text: 감성 분석을 수행할 고객 리뷰 원문. 1자 이상이어야 합니다.
    """

    review_text: str = Field(..., min_length=1, max_length=1000, description="분석할 고객 리뷰 텍스트")

    model_config = {
        "json_schema_extra": {
            "example": {
                "review_text": "배송이 너무 느려서 실망했어요. 상품 품질은 괜찮은데 포장이 엉망이었어요."
            }
        }
    }

class ReviewResponse(BaseModel):
    """POST /analyze 응답 스키마.
    Attributes:
        sentiment:   감성 분석 결과. 긍정 / 부정 / 중립 중 하나를 반환합니다.
        category:    리뷰의 주요 카테고리. 배송 / 품질 / 가격 / 서비스 / 기타 중 하나를 반환합니다.
        summary:     리뷰 내용을 한 문장으로 요약한 텍스트.
        confidence:  분석 결과에 대한 신뢰도. 0.0(낮음) ~ 1.0(높음) 범위의 실수값.
    """

    sentiment: str = Field(..., description="감성 분석 결과", examples=["긍정", "부정", "중립"])
    category: str = Field(..., description="리뷰 카테고리", examples=["배송", "품질", "가격", "서비스", "기타"])
    summary: str = Field(..., description="한 줄 요약 (1~2문장)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="분석 신뢰도 (0.0 ~ 1.0)")

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
