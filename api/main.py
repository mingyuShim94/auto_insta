"""
Instagram 텍스트 추출 FastAPI 애플리케이션
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import ExtractRequest, ExtractResponse, HealthResponse, PostData
from .services import InstagramService


# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="Instagram Text Extractor API",
    description="Instagram 게시물 링크에서 텍스트를 추출하는 API",
    version="1.0.0"
)

# CORS 설정 (Flutter 앱에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용, 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instagram 서비스 인스턴스
instagram_service = InstagramService()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """헬스체크 엔드포인트"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now()
    )


@app.post("/extract", response_model=ExtractResponse)
async def extract_text(request: ExtractRequest):
    """
    Instagram URL에서 텍스트 추출
    
    Args:
        request: Instagram URL이 포함된 요청 객체
        
    Returns:
        ExtractResponse: 추출 결과 또는 에러 정보
    """
    try:
        # URL을 문자열로 변환 (pydantic HttpUrl -> str)
        url = str(request.url)
        
        # 텍스트 추출 실행
        post_data = await instagram_service.extract_text(url)
        
        return ExtractResponse(
            success=True,
            data=post_data,
            error=None
        )
        
    except ValueError as e:
        # URL 유효성 검사 또는 게시물 찾기 실패
        return ExtractResponse(
            success=False,
            data=None,
            error=f"URL 처리 오류: {str(e)}"
        )
        
    except PermissionError as e:
        # 비공개 계정 접근 오류
        return ExtractResponse(
            success=False,
            data=None,
            error=f"접근 권한 오류: {str(e)}"
        )
        
    except ConnectionError as e:
        # 네트워크 연결 오류
        return ExtractResponse(
            success=False,
            data=None,
            error=f"네트워크 연결 오류: {str(e)}"
        )
        
    except Exception as e:
        # 기타 예상치 못한 오류
        return ExtractResponse(
            success=False,
            data=None,
            error=f"예상치 못한 오류: {str(e)}"
        )


@app.get("/")
async def root():
    """루트 경로 - API 정보 반환"""
    return {
        "message": "Instagram Text Extractor API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)