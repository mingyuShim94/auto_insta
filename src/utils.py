"""
유틸리티 함수 모듈
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
import os


def format_text_output(post_data: Dict[str, Any], show_metadata: bool = False) -> str:
    """게시물 데이터를 포맷팅하여 출력용 문자열로 변환

    Args:
        post_data (Dict[str, any]): 게시물 데이터
        show_metadata (bool): 메타데이터 포함 여부

    Returns:
        str: 포맷팅된 문자열
    """
    output_lines = []

    # 구분선
    output_lines.append("=" * 60)
    output_lines.append("📱 Instagram 게시물 본문")
    output_lines.append("=" * 60)

    # 메타데이터 (옵션)
    if show_metadata:
        output_lines.append(f"👤 작성자: @{post_data.get('username', 'Unknown')}")
        output_lines.append(f"❤️ 좋아요: {post_data.get('likes', 0):,}개")

        # 날짜 포맷팅
        post_date = post_data.get("date")
        if post_date:
            formatted_date = post_date.strftime("%Y년 %m월 %d일 %H:%M")
            output_lines.append(f"📅 게시일: {formatted_date}")

        media_count = post_data.get("media_count", 1)
        media_type = "📹 동영상" if post_data.get("is_video") else "📸 이미지"
        if media_count > 1:
            output_lines.append(f"📎 미디어: {media_type} 외 {media_count-1}개")
        else:
            output_lines.append(f"📎 미디어: {media_type}")

        output_lines.append("-" * 60)

    # 본문 텍스트
    text = post_data.get("text", "").strip()
    if text:
        output_lines.append("💬 본문:")
        output_lines.append(text)
    else:
        output_lines.append("💬 본문: (텍스트가 없습니다)")

    output_lines.append("=" * 60)

    return "\n".join(output_lines)


def save_to_file(
    post_data: Dict[str, Any],
    filename: Optional[str] = None,
    output_format: str = "txt",
) -> str:
    """게시물 데이터를 파일로 저장

    Args:
        post_data (Dict[str, any]): 게시물 데이터
        filename (Optional[str]): 저장할 파일명 (None이면 자동 생성)
        output_format (str): 출력 형식 ('txt', 'json')

    Returns:
        str: 저장된 파일 경로

    Raises:
        ValueError: 지원하지 않는 출력 형식인 경우
    """
    if output_format not in ["txt", "json"]:
        raise ValueError("지원하는 출력 형식: 'txt', 'json'")

    # 파일명 자동 생성
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = post_data.get("username", "unknown")
        filename = f"instagram_{username}_{timestamp}.{output_format}"

    # 출력 디렉토리 생성
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, filename)

    # 형식에 따라 저장
    with open(file_path, "w", encoding="utf-8") as f:
        if output_format == "txt":
            f.write(format_text_output(post_data, show_metadata=True))
        elif output_format == "json":
            # datetime 객체를 문자열로 변환
            json_data = post_data.copy()
            if "date" in json_data and json_data["date"]:
                json_data["date"] = json_data["date"].isoformat()
            f.write(json.dumps(json_data, ensure_ascii=False, indent=2))

    return file_path


def print_error_message(error_type: str, message: str) -> None:
    """에러 메시지를 포맷팅하여 출력

    Args:
        error_type (str): 에러 유형
        message (str): 에러 메시지
    """
    error_symbols = {
        "url_error": "🔗",
        "network_error": "🌐",
        "permission_error": "🔒",
        "general_error": "❌",
    }

    symbol = error_symbols.get(error_type, "❌")
    print(f"\n{symbol} 오류 발생:")
    print(f"   {message}")
    print()


def print_success_message(message: str) -> None:
    """성공 메시지를 포맷팅하여 출력

    Args:
        message (str): 성공 메시지
    """
    print(f"\n✅ {message}")
    print()


def get_user_confirmation(message: str) -> bool:
    """사용자에게 확인을 요청

    Args:
        message (str): 확인 메시지

    Returns:
        bool: 사용자 확인 결과 (y/n)
    """
    while True:
        response = input(f"{message} (y/n): ").lower().strip()
        if response in ["y", "yes", "ㅇ"]:
            return True
        elif response in ["n", "no", "ㄴ"]:
            return False
        else:
            print("'y' 또는 'n'으로 답해주세요.")


def truncate_text(text: str, max_length: int = 100) -> str:
    """텍스트를 지정된 길이로 자르기

    Args:
        text (str): 원본 텍스트
        max_length (int): 최대 길이

    Returns:
        str: 잘린 텍스트
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."


def validate_file_path(file_path: str) -> bool:
    """파일 경로 유효성 검증

    Args:
        file_path (str): 검증할 파일 경로

    Returns:
        bool: 유효한 파일 경로인지 여부
    """
    try:
        # 디렉토리 존재 확인
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            return False

        # 파일명 유효성 확인
        filename = os.path.basename(file_path)
        invalid_chars = '<>:"|?*'
        if any(char in filename for char in invalid_chars):
            return False

        return True
    except Exception:
        return False
