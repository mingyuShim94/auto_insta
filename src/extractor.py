"""
Instagram 게시물 텍스트 추출 모듈
"""

import re
import time
from typing import Dict
from urllib.parse import urlparse
import instaloader


class InstagramTextExtractor:
    """Instagram 게시물에서 텍스트를 추출하는 클래스"""

    def __init__(self):
        """Instaloader 인스턴스 초기화"""
        self.loader = instaloader.Instaloader()
        # User-Agent 설정으로 차단 방지
        user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        self.loader.context._session.headers.update({"User-Agent": user_agent})

    def validate_url(self, url: str) -> bool:
        """Instagram URL 유효성 검증

        Args:
            url (str): 검증할 Instagram URL

        Returns:
            bool: 유효한 Instagram URL인지 여부
        """
        try:
            parsed_url = urlparse(url)

            # Instagram 도메인 확인
            if parsed_url.netloc not in ["www.instagram.com", "instagram.com"]:
                return False

            # 게시물 경로 패턴 확인 (/p/, /reel/, /tv/)
            path_pattern = r"^/(p|reel|tv)/([A-Za-z0-9_-]+)/?"
            if not re.match(path_pattern, parsed_url.path):
                return False

            return True
        except Exception:
            return False

    def extract_shortcode(self, url: str) -> str:
        """URL에서 shortcode 추출

        Args:
            url (str): Instagram 게시물 URL

        Returns:
            str: 추출된 shortcode

        Raises:
            ValueError: 유효하지 않은 URL인 경우
        """
        if not self.validate_url(url):
            raise ValueError("유효하지 않은 Instagram URL입니다.")

        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")

        if len(path_parts) >= 2:
            return path_parts[1]

        raise ValueError("URL에서 shortcode를 추출할 수 없습니다.")

    def get_post_text(self, url: str, title: str = "미정", max_retries: int = 5, retry_delay: int = 5) -> Dict[str, any]:
        """게시물에서 텍스트 및 메타데이터 추출 (재시도 기능 포함)

        Args:
            url (str): Instagram 게시물 URL
            title (str): 게시물 제목 (기본값: "미정")
            max_retries (int): 최대 재시도 횟수 (기본값: 5)
            retry_delay (int): 초기 재시도 대기시간 (초, 기본값: 5)

        Returns:
            Dict[str, any]: 추출된 정보를 담은 딕셔너리
                - title: 게시물 제목
                - text: 본문 텍스트
                - username: 작성자명
                - likes: 좋아요 수
                - date: 게시 날짜
                - media_count: 미디어 개수
                - is_video: 동영상 여부

        Raises:
            ValueError: URL이 유효하지 않거나 게시물을 찾을 수 없는 경우
            ConnectionError: 네트워크 연결 문제
            PermissionError: 접근 권한이 없는 경우 (Private 계정)
        """
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                shortcode = self.extract_shortcode(url)

                # Instaloader를 사용해 게시물 정보 가져오기
                post = instaloader.Post.from_shortcode(self.loader.context, shortcode)

                # 텍스트 추출 및 정제
                caption_text = post.caption or ""

                return {
                    "title": title,
                    "text": self._clean_text(caption_text),
                    "username": post.owner_username,
                    "likes": post.likes,
                    "date": post.date,
                    "media_count": post.mediacount,
                    "is_video": post.is_video,
                    "url": url,
                }

            except instaloader.exceptions.PostChangedException:
                raise ValueError("게시물이 삭제되었거나 존재하지 않습니다.")
            except instaloader.exceptions.ProfileNotExistsException:
                raise ValueError("존재하지 않는 계정입니다.")
            except instaloader.exceptions.PrivateProfileNotFollowedException:
                raise PermissionError("비공개 계정입니다. 로그인이 필요합니다.")
            except instaloader.exceptions.ConnectionException as e:
                last_error = e
                if self._is_rate_limit_error(str(e)) and attempt < max_retries:
                    wait_time = retry_delay * (2 ** attempt)  # 점진적 백오프
                    print(f"      ⚠️ Rate limit 감지 ({attempt+1}/{max_retries+1}). {wait_time}초 후 재시도...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ConnectionError(f"네트워크 연결 오류: {str(e)}")
            except Exception as e:
                last_error = e
                error_msg = str(e)
                if self._is_rate_limit_error(error_msg) and attempt < max_retries:
                    wait_time = retry_delay * (2 ** attempt)  # 점진적 백오프
                    print(f"      ⚠️ Instagram API 제한 감지 ({attempt+1}/{max_retries+1}). {wait_time}초 후 재시도...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ValueError(f"게시물 정보를 가져오는 중 오류 발생: {error_msg}")
        
        # 모든 재시도가 실패한 경우
        if last_error:
            if isinstance(last_error, instaloader.exceptions.ConnectionException):
                raise ConnectionError(f"네트워크 연결 오류 (재시도 {max_retries}회 실패): {str(last_error)}")
            else:
                raise ValueError(f"게시물 정보를 가져오는 중 오류 발생 (재시도 {max_retries}회 실패): {str(last_error)}")

    def _is_rate_limit_error(self, error_message: str) -> bool:
        """Rate limit 관련 에러인지 확인
        
        Args:
            error_message (str): 에러 메시지
            
        Returns:
            bool: Rate limit 에러 여부
        """
        rate_limit_indicators = [
            "403",
            "forbidden",
            "rate limit",
            "too many requests",
            "graphql/query",
            "temporarily blocked"
        ]
        
        error_lower = error_message.lower()
        return any(indicator in error_lower for indicator in rate_limit_indicators)

    def _clean_text(self, text: str) -> str:
        """텍스트 정제

        Args:
            text (str): 원본 텍스트

        Returns:
            str: 정제된 텍스트
        """
        if not text:
            return ""

        # 불필요한 공백 제거
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def extract_hashtags(self, text: str) -> list:
        """텍스트에서 해시태그 추출

        Args:
            text (str): 추출할 텍스트

        Returns:
            list: 해시태그 리스트
        """
        hashtag_pattern = r"#[가-힣\w]+"
        return re.findall(hashtag_pattern, text)

    def extract_mentions(self, text: str) -> list:
        """텍스트에서 멘션 추출

        Args:
            text (str): 추출할 텍스트

        Returns:
            list: 멘션 리스트
        """
        mention_pattern = r"@\w+"
        return re.findall(mention_pattern, text)
