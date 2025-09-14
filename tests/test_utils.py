"""
utils.py 테스트
"""

import pytest
import os
import tempfile
import json
from datetime import datetime
from unittest.mock import patch, mock_open, Mock

from src.utils import (
    format_text_output,
    save_to_file,
    truncate_text,
    validate_file_path,
    get_user_confirmation,
)


class TestUtils:
    """유틸리티 함수들 테스트"""

    def setup_method(self):
        """각 테스트 메서드 실행 전 설정"""
        self.sample_post_data = {
            "text": "테스트 게시물 본문입니다. #테스트 #인스타그램",
            "username": "test_user",
            "likes": 150,
            "date": datetime(2023, 6, 15, 14, 30, 0),
            "media_count": 1,
            "is_video": False,
            "url": "https://www.instagram.com/p/ABC123/",
        }

    def test_format_text_output_without_metadata(self):
        """메타데이터 없는 텍스트 포맷팅 테스트"""
        result = format_text_output(self.sample_post_data, show_metadata=False)

        # 기본 구조 확인
        assert "Instagram 게시물 본문" in result
        assert "테스트 게시물 본문입니다. #테스트 #인스타그램" in result

        # 메타데이터가 포함되지 않았는지 확인
        assert "작성자:" not in result
        assert "좋아요:" not in result
        assert "게시일:" not in result

    def test_format_text_output_with_metadata(self):
        """메타데이터 포함 텍스트 포맷팅 테스트"""
        result = format_text_output(self.sample_post_data, show_metadata=True)

        # 메타데이터 포함 확인
        assert "작성자: @test_user" in result
        assert "좋아요: 150개" in result
        assert "2023년 06월 15일 14:30" in result
        assert "이미지" in result
        assert "테스트 게시물 본문입니다. #테스트 #인스타그램" in result

    def test_format_text_output_empty_text(self):
        """빈 텍스트 포맷팅 테스트"""
        empty_post_data = self.sample_post_data.copy()
        empty_post_data["text"] = ""

        result = format_text_output(empty_post_data, show_metadata=False)
        assert "(텍스트가 없습니다)" in result

    def test_format_text_output_video_content(self):
        """동영상 컨텐츠 포맷팅 테스트"""
        video_post_data = self.sample_post_data.copy()
        video_post_data["is_video"] = True
        video_post_data["media_count"] = 3

        result = format_text_output(video_post_data, show_metadata=True)
        assert "동영상 외 2개" in result

    @patch("src.utils.os.makedirs")
    @patch("src.utils.open", new_callable=mock_open)
    def test_save_to_file_txt_format(self, mock_file, mock_makedirs):
        """TXT 형식 파일 저장 테스트"""
        with patch("src.utils.os.path.exists", return_value=False):
            result_path = save_to_file(self.sample_post_data, "test_output.txt", "txt")

        # 디렉토리 생성 확인
        mock_makedirs.assert_called_once_with("outputs")

        # 파일 경로 확인
        assert result_path == "outputs/test_output.txt"

        # 파일 쓰기 확인
        mock_file.assert_called_once_with(
            "outputs/test_output.txt", "w", encoding="utf-8"
        )

    @patch("src.utils.os.makedirs")
    @patch("src.utils.open", new_callable=mock_open)
    def test_save_to_file_json_format(self, mock_file, mock_makedirs):
        """JSON 형식 파일 저장 테스트"""
        with patch("src.utils.os.path.exists", return_value=False):
            result_path = save_to_file(
                self.sample_post_data, "test_output.json", "json"
            )

        assert result_path == "outputs/test_output.json"
        mock_file.assert_called_once_with(
            "outputs/test_output.json", "w", encoding="utf-8"
        )

    def test_save_to_file_invalid_format(self):
        """지원하지 않는 형식 테스트"""
        with pytest.raises(ValueError, match="지원하는 출력 형식"):
            save_to_file(self.sample_post_data, "test.xml", "xml")

    @patch("src.utils.datetime")
    def test_save_to_file_auto_filename(self, mock_datetime):
        """자동 파일명 생성 테스트"""
        # Mock 현재 시간과 strftime 메서드
        mock_now = Mock()
        mock_now.strftime.return_value = "20230615_103045"
        mock_datetime.now.return_value = mock_now

        with patch("src.utils.os.makedirs"), patch(
            "src.utils.open", mock_open()
        ), patch("src.utils.os.path.exists", return_value=False):

            result_path = save_to_file(self.sample_post_data, None, "txt")

            # 자동 생성된 파일명 패턴 확인
            assert "instagram_test_user_" in result_path
            assert result_path.endswith(".txt")

    def test_truncate_text_normal(self):
        """일반 텍스트 자르기 테스트"""
        text = "이것은 긴 텍스트입니다."
        result = truncate_text(text, 10)
        assert result == "이것은 긴 텍..."
        assert len(result) == 10

    def test_truncate_text_short(self):
        """짧은 텍스트 자르기 테스트"""
        text = "짧은글"
        result = truncate_text(text, 10)
        assert result == "짧은글"

    def test_truncate_text_exact_length(self):
        """정확한 길이 텍스트 자르기 테스트"""
        text = "정확히열글자임"
        result = truncate_text(text, 7)
        assert result == "정확히열글자임"

    def test_validate_file_path_valid(self):
        """유효한 파일 경로 테스트"""
        valid_paths = [
            "test.txt",
            "folder/test.txt",
            "/absolute/path/test.txt",
            "한글파일명.txt",
        ]

        for path in valid_paths:
            with patch("src.utils.os.path.exists", return_value=True):
                assert validate_file_path(path), f"경로가 유효해야 합니다: {path}"

    def test_validate_file_path_invalid_chars(self):
        """유효하지 않은 문자 포함 파일 경로 테스트"""
        invalid_paths = [
            "test<.txt",
            "test>.txt",
            "test:.txt",
            'test".txt',
            "test|.txt",
            "test?.txt",
            "test*.txt",
        ]

        for path in invalid_paths:
            assert not validate_file_path(path), f"경로가 무효해야 합니다: {path}"

    @patch("builtins.input", side_effect=["y"])
    def test_get_user_confirmation_yes(self, mock_input):
        """사용자 확인 - 예 테스트"""
        result = get_user_confirmation("계속하시겠습니까?")
        assert result is True

    @patch("builtins.input", side_effect=["n"])
    def test_get_user_confirmation_no(self, mock_input):
        """사용자 확인 - 아니오 테스트"""
        result = get_user_confirmation("계속하시겠습니까?")
        assert result is False

    @patch("builtins.input", side_effect=["invalid", "y"])
    def test_get_user_confirmation_retry(self, mock_input):
        """잘못된 입력 후 재시도 테스트"""
        result = get_user_confirmation("계속하시겠습니까?")
        assert result is True
        assert mock_input.call_count == 2
