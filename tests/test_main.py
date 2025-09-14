"""
main.py 테스트
"""

import argparse
from unittest.mock import Mock, patch
from io import StringIO

from src.main import parse_arguments, process_single_url


class TestMain:
    """메인 함수들 테스트"""

    def test_parse_arguments_url_only(self):
        """URL만 제공된 경우 인수 파싱 테스트"""
        test_args = ["https://www.instagram.com/p/ABC123/"]

        with patch("sys.argv", ["main.py"] + test_args):
            args = parse_arguments()

        assert args.url == "https://www.instagram.com/p/ABC123/"
        assert args.metadata is False
        assert args.save is None
        assert args.output is None
        assert args.quiet is False

    def test_parse_arguments_with_options(self):
        """모든 옵션과 함께 인수 파싱 테스트"""
        test_args = [
            "https://www.instagram.com/p/ABC123/",
            "--metadata",
            "--save",
            "json",
            "--output",
            "my_output",
            "--quiet",
        ]

        with patch("sys.argv", ["main.py"] + test_args):
            args = parse_arguments()

        assert args.url == "https://www.instagram.com/p/ABC123/"
        assert args.metadata is True
        assert args.save == "json"
        assert args.output == "my_output"
        assert args.quiet is True

    def test_parse_arguments_no_url(self):
        """URL이 제공되지 않은 경우 테스트"""
        with patch("sys.argv", ["main.py"]):
            args = parse_arguments()

        assert args.url is None

    @patch("src.main.InstagramTextExtractor")
    @patch("src.main.format_text_output")
    def test_process_single_url_success(self, mock_format, mock_extractor_class):
        """성공적인 URL 처리 테스트"""
        # Mock 설정
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor

        mock_post_data = {
            "text": "테스트 본문",
            "username": "test_user",
            "likes": 100,
            "date": None,
            "media_count": 1,
            "is_video": False,
        }
        mock_extractor.get_post_text.return_value = mock_post_data

        mock_format.return_value = "포맷된 출력"

        # 테스트 실행
        args = argparse.Namespace(metadata=True, save=None, output=None, quiet=False)

        with patch("builtins.print"):
            result = process_single_url(
                mock_extractor, "https://www.instagram.com/p/ABC123/", args
            )

        # 검증
        assert result is True
        mock_extractor.get_post_text.assert_called_once_with(
            "https://www.instagram.com/p/ABC123/"
        )
        mock_format.assert_called_once_with(mock_post_data, show_metadata=True)

    @patch("src.main.InstagramTextExtractor")
    def test_process_single_url_value_error(self, mock_extractor_class):
        """ValueError 처리 테스트"""
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.get_post_text.side_effect = ValueError("잘못된 URL")

        args = argparse.Namespace(metadata=False, save=None, output=None, quiet=False)

        with patch("src.main.print_error_message") as mock_error:
            result = process_single_url(mock_extractor, "invalid_url", args)

        assert result is False
        mock_error.assert_called_once_with("url_error", "잘못된 URL")

    @patch("src.main.InstagramTextExtractor")
    def test_process_single_url_permission_error(self, mock_extractor_class):
        """PermissionError 처리 테스트"""
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.get_post_text.side_effect = PermissionError("비공개 계정")

        args = argparse.Namespace(metadata=False, save=None, output=None, quiet=False)

        with patch("src.main.print_error_message") as mock_error:
            result = process_single_url(mock_extractor, "private_url", args)

        assert result is False
        mock_error.assert_called_once_with("permission_error", "비공개 계정")

    @patch("src.main.InstagramTextExtractor")
    def test_process_single_url_connection_error(self, mock_extractor_class):
        """ConnectionError 처리 테스트"""
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.get_post_text.side_effect = ConnectionError("네트워크 오류")

        args = argparse.Namespace(metadata=False, save=None, output=None, quiet=False)

        with patch("src.main.print_error_message") as mock_error:
            result = process_single_url(mock_extractor, "network_fail_url", args)

        assert result is False
        mock_error.assert_called_once_with("network_error", "네트워크 오류")

    @patch("src.main.InstagramTextExtractor")
    @patch("src.main.save_to_file")
    def test_process_single_url_with_save(self, mock_save, mock_extractor_class):
        """파일 저장 옵션 테스트"""
        # Mock 설정
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor

        mock_post_data = {"text": "테스트 본문"}
        mock_extractor.get_post_text.return_value = mock_post_data

        mock_save.return_value = "outputs/saved_file.txt"

        # 테스트 실행
        args = argparse.Namespace(
            metadata=False, save="txt", output="custom_name", quiet=False
        )

        with patch("builtins.print"), patch("src.main.format_text_output"), patch(
            "src.main.print_success_message"
        ) as mock_success:

            result = process_single_url(mock_extractor, "test_url", args)

        # 검증
        assert result is True
        mock_save.assert_called_once_with(mock_post_data, "custom_name.txt", "txt")
        mock_success.assert_called_once()

    @patch("src.main.InstagramTextExtractor")
    def test_process_single_url_quiet_mode(self, mock_extractor_class):
        """Quiet 모드 테스트"""
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor

        mock_post_data = {"text": "테스트 본문입니다"}
        mock_extractor.get_post_text.return_value = mock_post_data

        args = argparse.Namespace(metadata=False, save=None, output=None, quiet=True)

        # stdout 캡처
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            result = process_single_url(mock_extractor, "test_url", args)

        # 검증
        assert result is True
        output = captured_output.getvalue()
        assert "테스트 본문입니다" in output
        # quiet 모드에서는 포맷팅된 출력이 없어야 함
        assert "Instagram 게시물 본문" not in output
