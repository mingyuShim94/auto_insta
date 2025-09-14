"""
extractor.py 테스트
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.extractor import InstagramTextExtractor


class TestInstagramTextExtractor:
    """InstagramTextExtractor 클래스 테스트"""

    def setup_method(self):
        """각 테스트 메서드 실행 전 설정"""
        self.extractor = InstagramTextExtractor()

    def test_validate_url_valid_post(self):
        """유효한 게시물 URL 테스트"""
        valid_urls = [
            "https://www.instagram.com/p/ABC123/",
            "https://instagram.com/p/XYZ789/",
            "http://www.instagram.com/p/DEF456/",
            "https://www.instagram.com/reel/GHI789/",
            "https://instagram.com/tv/JKL012/",
        ]

        for url in valid_urls:
            assert self.extractor.validate_url(url), f"URL이 유효해야 합니다: {url}"

    def test_validate_url_invalid_post(self):
        """유효하지 않은 URL 테스트"""
        invalid_urls = [
            "https://facebook.com/p/ABC123/",
            "https://www.instagram.com/user/",
            "https://www.instagram.com/",
            "not_a_url",
            "",
            "https://www.instagram.com/p/",
            "https://www.instagram.com/invalid/",
        ]

        for url in invalid_urls:
            assert not self.extractor.validate_url(url), f"URL이 무효해야 합니다: {url}"

    def test_extract_shortcode_valid_url(self):
        """유효한 URL에서 shortcode 추출 테스트"""
        test_cases = [
            ("https://www.instagram.com/p/ABC123/", "ABC123"),
            ("https://instagram.com/reel/XYZ789/", "XYZ789"),
            ("https://www.instagram.com/tv/DEF456/", "DEF456"),
        ]

        for url, expected_shortcode in test_cases:
            result = self.extractor.extract_shortcode(url)
            assert result == expected_shortcode

    def test_extract_shortcode_invalid_url(self):
        """유효하지 않은 URL에서 shortcode 추출 시 예외 발생 테스트"""
        invalid_urls = [
            "https://facebook.com/p/ABC123/",
            "https://www.instagram.com/user/",
            "not_a_url",
        ]

        for url in invalid_urls:
            with pytest.raises(ValueError):
                self.extractor.extract_shortcode(url)

    def test_clean_text(self):
        """텍스트 정제 기능 테스트"""
        test_cases = [
            ("  Hello   World  ", "Hello World"),
            ("Text\n\nwith\n\nmultiple\n\nspaces", "Text with multiple spaces"),
            ("", ""),
            ("   ", ""),
            ("Normal text", "Normal text"),
        ]

        for input_text, expected_output in test_cases:
            result = self.extractor._clean_text(input_text)
            assert result == expected_output

    def test_extract_hashtags(self):
        """해시태그 추출 테스트"""
        test_text = "이것은 #테스트 게시물입니다 #instagram #소셜미디어 #한글해시태그"
        expected_hashtags = ["#테스트", "#instagram", "#소셜미디어", "#한글해시태그"]

        result = self.extractor.extract_hashtags(test_text)
        assert result == expected_hashtags

    def test_extract_mentions(self):
        """멘션 추출 테스트"""
        test_text = "안녕하세요 @user1 그리고 @user2 입니다!"
        expected_mentions = ["@user1", "@user2"]

        result = self.extractor.extract_mentions(test_text)
        assert result == expected_mentions

    @patch("src.extractor.instaloader.Post.from_shortcode")
    def test_get_post_text_success(self, mock_from_shortcode):
        """게시물 텍스트 추출 성공 테스트"""
        # Mock 게시물 객체 생성
        mock_post = Mock()
        mock_post.caption = "테스트 게시물 본문입니다 #테스트"
        mock_post.owner_username = "test_user"
        mock_post.likes = 100
        mock_post.date = datetime(2023, 1, 1, 12, 0, 0)
        mock_post.mediacount = 1
        mock_post.is_video = False

        mock_from_shortcode.return_value = mock_post

        url = "https://www.instagram.com/p/ABC123/"
        result = self.extractor.get_post_text(url)

        # 결과 검증
        assert result["text"] == "테스트 게시물 본문입니다 #테스트"
        assert result["username"] == "test_user"
        assert result["likes"] == 100
        assert result["date"] == datetime(2023, 1, 1, 12, 0, 0)
        assert result["media_count"] == 1
        assert result["is_video"] is False
        assert result["url"] == url

    @patch("src.extractor.instaloader.Post.from_shortcode")
    def test_get_post_text_empty_caption(self, mock_from_shortcode):
        """빈 캡션 게시물 테스트"""
        mock_post = Mock()
        mock_post.caption = None
        mock_post.owner_username = "test_user"
        mock_post.likes = 50
        mock_post.date = datetime(2023, 1, 1, 12, 0, 0)
        mock_post.mediacount = 1
        mock_post.is_video = True

        mock_from_shortcode.return_value = mock_post

        url = "https://www.instagram.com/p/ABC123/"
        result = self.extractor.get_post_text(url)

        assert result["text"] == ""
        assert result["is_video"] is True

    @patch("src.extractor.instaloader.Post.from_shortcode")
    def test_get_post_text_post_not_exists(self, mock_from_shortcode):
        """존재하지 않는 게시물 테스트"""
        import instaloader.exceptions

        mock_from_shortcode.side_effect = instaloader.exceptions.PostChangedException()

        url = "https://www.instagram.com/p/NOTEXIST/"

        with pytest.raises(ValueError, match="게시물이 삭제되었거나 존재하지 않습니다"):
            self.extractor.get_post_text(url)

    @patch("src.extractor.instaloader.Post.from_shortcode")
    def test_get_post_text_private_profile(self, mock_from_shortcode):
        """비공개 계정 게시물 테스트"""
        import instaloader.exceptions

        mock_from_shortcode.side_effect = (
            instaloader.exceptions.PrivateProfileNotFollowedException()
        )

        url = "https://www.instagram.com/p/PRIVATE/"

        with pytest.raises(PermissionError, match="비공개 계정입니다"):
            self.extractor.get_post_text(url)

    @patch("src.extractor.instaloader.Post.from_shortcode")
    def test_get_post_text_network_error(self, mock_from_shortcode):
        """네트워크 오류 테스트"""
        import instaloader.exceptions

        mock_from_shortcode.side_effect = instaloader.exceptions.ConnectionException(
            "Network error"
        )

        url = "https://www.instagram.com/p/ABC123/"

        with pytest.raises(ConnectionError, match="네트워크 연결 오류"):
            self.extractor.get_post_text(url)
