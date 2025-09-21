"""
Instagram 텍스트 추출 서비스
기존 InstagramTextExtractor를 FastAPI용으로 래핑
"""

import sys
import os
from typing import Dict, Any

# 상위 디렉토리의 src 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extractor import InstagramTextExtractor
from .models import PostData


class InstagramService:
    """Instagram 텍스트 추출 서비스 클래스"""
    
    def __init__(self):
        """Instagram 텍스트 추출기 초기화"""
        self.extractor = InstagramTextExtractor()
    
    async def extract_text(self, url: str) -> PostData:
        """
        Instagram URL에서 텍스트 추출
        
        Args:
            url (str): Instagram 게시물 URL
            
        Returns:
            PostData: 추출된 게시물 데이터
            
        Raises:
            ValueError: URL이 유효하지 않거나 게시물을 찾을 수 없는 경우
            ConnectionError: 네트워크 연결 문제
            PermissionError: 접근 권한이 없는 경우 (Private 계정)
        """
        try:
            # 기존 InstagramTextExtractor 사용
            post_data = self.extractor.get_post_text(url)
            
            # Pydantic 모델로 변환
            return PostData(
                text=post_data.get("text", ""),
                username=post_data.get("username", ""),
                likes=post_data.get("likes", 0),
                date=post_data.get("date"),
                media_count=post_data.get("media_count", 1),
                is_video=post_data.get("is_video", False),
                url=post_data.get("url", url)
            )
            
        except Exception as e:
            # 에러를 그대로 re-raise하여 상위에서 처리하도록 함
            raise e