"""
FastAPI용 Pydantic 모델 정의
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class ExtractRequest(BaseModel):
    """텍스트 추출 요청 모델"""
    url: HttpUrl = Field(..., description="Instagram 게시물 URL")


class PostData(BaseModel):
    """Instagram 게시물 데이터 모델"""
    text: str = Field(..., description="추출된 본문 텍스트")
    username: str = Field(..., description="작성자 사용자명")
    likes: int = Field(..., description="좋아요 수")
    date: Optional[datetime] = Field(None, description="게시 날짜")
    media_count: int = Field(..., description="미디어 개수")
    is_video: bool = Field(..., description="동영상 여부")
    url: str = Field(..., description="원본 URL")


class ExtractResponse(BaseModel):
    """텍스트 추출 응답 모델"""
    success: bool = Field(..., description="성공 여부")
    data: Optional[PostData] = Field(None, description="게시물 데이터")
    error: Optional[str] = Field(None, description="에러 메시지")


class HealthResponse(BaseModel):
    """헬스체크 응답 모델"""
    status: str = Field(..., description="서비스 상태")
    timestamp: datetime = Field(..., description="응답 시각")