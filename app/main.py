from contextlib import asynccontextmanager
import logging


from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.gemini_client import ReviewAnalyzer
from app.schema import ReviewRequest, ReviewResponse


from pathlib import Path
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path= env_path, override=True) # True: .env 파일이 항상 시스템 환경변수를 덮어씀

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    try :
        app.state.analyzer = ReviewAnalyzer()
        logger.info("분석기 초기화 완료")
    except ValueError as e:
        logger.error("분석기 초기화 실패") 
        raise

    yield

    logger.info("서비스 종료 중...")


app = FastAPI(
    title="고객 리뷰 분석 API",
    description="Gemini LLM 기반 고객 리뷰 감성 분석 API",
    version="1.0.5",
    lifespan= lifespan
)

@app.get('/health')
def health_check():
    return {"status" : "healthy"}

@app.post("/analyze", response_model= ReviewResponse)
def analyze_review(request : ReviewRequest):

    try:

        result = app.state.analyzer.analyze(request.review_text)
        return ReviewResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))