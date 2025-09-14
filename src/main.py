#!/usr/bin/env python3
"""
Instagram 게시물 텍스트 추출기 - 메인 CLI 인터페이스
"""

import sys
import argparse
import time
import os
from typing import Optional, List

from .extractor import InstagramTextExtractor
from .utils import (
    format_text_output,
    save_to_file,
    print_error_message,
    print_success_message,
    get_user_confirmation,
)


def parse_arguments() -> argparse.Namespace:
    """명령줄 인수 파싱"""
    parser = argparse.ArgumentParser(
        description="Instagram 게시물 링크에서 본문 텍스트를 추출합니다.",
        epilog="예시: python main.py https://www.instagram.com/p/ABC123/",
    )

    parser.add_argument("url", nargs="?", help="Instagram 게시물 URL")

    parser.add_argument(
        "--metadata",
        "-m",
        action="store_true",
        help="메타데이터 포함 (작성자, 좋아요 수, 날짜 등)",
    )

    parser.add_argument(
        "--save",
        "-s",
        metavar="FORMAT",
        choices=["txt", "json"],
        help="결과를 파일로 저장 (txt 또는 json 형식)",
    )

    parser.add_argument(
        "--output", "-o", metavar="FILENAME", help="저장할 파일명 (확장자 제외)"
    )

    parser.add_argument(
        "--quiet", "-q", action="store_true", help="최소한의 출력만 표시"
    )

    parser.add_argument(
        "--batch-file",
        "-b",
        metavar="FILEPATH",
        help="URL 목록이 포함된 파일 경로",
    )

    parser.add_argument(
        "--combined-output",
        "-c",
        action="store_true",
        help="모든 결과를 하나의 통합 파일로 저장",
    )

    parser.add_argument(
        "--delay",
        "-d",
        type=int,
        default=3,
        help="URL 처리 간 대기시간 (초, 기본값: 3초)",
    )

    return parser.parse_args()


def read_urls_from_file(file_path: str) -> List[str]:
    """파일에서 URL 목록을 읽어오기

    Args:
        file_path (str): URL 목록 파일 경로

    Returns:
        List[str]: URL 목록

    Raises:
        FileNotFoundError: 파일이 존재하지 않는 경우
        ValueError: 파일 형식이 잘못된 경우
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        urls = []
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            # 빈 줄이나 주석(#으로 시작) 제외
            if line and not line.startswith('#'):
                if line.startswith('https://') or line.startswith('http://'):
                    urls.append(line)
                else:
                    print(f"⚠️ 라인 {line_num}: 유효하지 않은 URL 형식 - {line}")

        if not urls:
            raise ValueError("유효한 URL이 없습니다.")

        return urls

    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        raise ValueError(f"파일 읽기 오류: {str(e)}")


def save_combined_results(results: List[dict], output_format: str = 'txt') -> str:
    """배치 처리 결과를 통합 파일로 저장

    Args:
        results (List[dict]): 처리 결과 목록
        output_format (str): 출력 형식 ('txt' 또는 'json')

    Returns:
        str: 저장된 파일 경로
    """
    from datetime import datetime
    from .utils import save_to_file
    import json

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if output_format == 'txt':
        # 텍스트 형식으로 통합
        combined_text = []
        combined_text.append("=" * 80)
        combined_text.append("📱 Instagram 배치 처리 결과")
        combined_text.append(f"📅 처리일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}")
        combined_text.append(f"📊 총 처리 건수: {len(results)}개")
        combined_text.append("=" * 80)
        combined_text.append("")

        for i, result in enumerate(results, 1):
            combined_text.append(f"[{i:02d}] {result['url']}")
            combined_text.append(f"👤 작성자: @{result.get('username', 'Unknown')}")
            combined_text.append(f"❤️ 좋아요: {result.get('likes', 0):,}개")
            if result.get('date'):
                date_str = result['date'].strftime('%Y년 %m월 %d일 %H:%M')
                combined_text.append(f"📅 게시일: {date_str}")
            combined_text.append("")
            combined_text.append("💬 본문:")
            combined_text.append(result.get('text', '(텍스트 없음)'))
            combined_text.append("")
            combined_text.append("-" * 60)
            combined_text.append("")

        # 파일 저장
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = f"instagram_batch_combined_{timestamp}.txt"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(combined_text))

    elif output_format == 'json':
        # JSON 형식으로 통합
        batch_data = {
            'processed_at': datetime.now().isoformat(),
            'total_count': len(results),
            'results': []
        }

        for result in results:
            json_result = result.copy()
            if 'date' in json_result and json_result['date']:
                json_result['date'] = json_result['date'].isoformat()
            batch_data['results'].append(json_result)

        # 파일 저장
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = f"instagram_batch_combined_{timestamp}.json"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)

    return file_path


def process_batch_urls(extractor: InstagramTextExtractor, urls: List[str], args: argparse.Namespace) -> List[dict]:
    """배치로 여러 URL 처리

    Args:
        extractor: Instagram 텍스트 추출기
        urls: 처리할 URL 목록
        args: 명령줄 인수

    Returns:
        List[dict]: 처리 성공한 결과 목록
    """
    results = []
    failed_urls = []
    total_count = len(urls)

    print(f"🚀 배치 처리 시작: 총 {total_count}개 URL")
    print(f"⏱️ URL 간 대기시간: {args.delay}초")
    print("=" * 60)

    for i, url in enumerate(urls, 1):
        print(f"\n[{i:02d}/{total_count:02d}] 처리 중: {url}")

        try:
            # 첫 번째 URL이 아니면 대기
            if i > 1:
                print(f"⏳ {args.delay}초 대기 중...")
                time.sleep(args.delay)

            # 텍스트 추출
            post_data = extractor.get_post_text(url)
            results.append(post_data)

            # 성공 메시지
            username = post_data.get('username', 'Unknown')
            likes = post_data.get('likes', 0)
            print(f"✅ 성공: @{username} ({likes:,}개 좋아요)")

            # 개별 파일 저장 (combined-output이 아닌 경우)
            if args.save and not args.combined_output:
                filename = f"batch_{i:02d}_{username}_{int(time.time())}.{args.save}"
                file_path = save_to_file(post_data, filename, args.save)
                print(f"💾 저장: {file_path}")

        except Exception as e:
            error_msg = str(e)
            failed_urls.append({'url': url, 'error': error_msg})
            print(f"❌ 실패: {error_msg}")
            continue

    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 배치 처리 완료")
    print(f"✅ 성공: {len(results)}개")
    print(f"❌ 실패: {len(failed_urls)}개")

    # 실패한 URL 목록 저장
    if failed_urls:
        print("\n❌ 실패한 URL 목록:")
        for failed in failed_urls:
            print(f"   {failed['url']} - {failed['error']}")

        # 실패 목록을 파일로 저장
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = int(time.time())
        failed_file = os.path.join(output_dir, f"failed_urls_{timestamp}.txt")
        with open(failed_file, 'w', encoding='utf-8') as f:
            f.write("# 실패한 Instagram URL 목록\\n")
            f.write(f"# 처리일시: {time.strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
            for failed in failed_urls:
                f.write(f"{failed['url']}  # 오류: {failed['error']}\\n")
        print(f"💾 실패 목록 저장: {failed_file}")

    return results


def get_url_interactively() -> Optional[str]:
    """대화형으로 URL 입력받기"""
    print("🎯 Instagram 게시물 텍스트 추출기")
    print("-" * 40)
    print("Instagram 게시물 링크를 입력하세요.")
    print("(종료하려면 'quit' 또는 'exit' 입력)")
    print()

    while True:
        url = input("📱 Instagram URL: ").strip()

        if url.lower() in ["quit", "exit", "q"]:
            return None

        if url:
            return url

        print("URL을 입력해주세요.")


def process_single_url(
    extractor: InstagramTextExtractor, url: str, args: argparse.Namespace
) -> bool:
    """단일 URL 처리

    Returns:
        bool: 성공 여부
    """
    try:
        # 텍스트 추출
        if not args.quiet:
            print("📥 게시물 정보를 가져오는 중...")

        post_data = extractor.get_post_text(url)

        # 콘솔 출력
        if not args.quiet:
            print(format_text_output(post_data, show_metadata=args.metadata))
        else:
            # quiet 모드에서는 본문만 출력
            print(post_data.get("text", ""))

        # 파일 저장
        if args.save:
            filename = None
            if args.output:
                filename = f"{args.output}.{args.save}"

            file_path = save_to_file(post_data, filename, args.save)
            if not args.quiet:
                print_success_message(f"결과를 {file_path}에 저장했습니다.")

        return True

    except ValueError as e:
        print_error_message("url_error", str(e))
        return False
    except PermissionError as e:
        print_error_message("permission_error", str(e))
        return False
    except ConnectionError as e:
        print_error_message("network_error", str(e))
        return False
    except Exception as e:
        print_error_message("general_error", f"예상치 못한 오류: {str(e)}")
        return False


def interactive_mode():
    """대화형 모드"""
    extractor = InstagramTextExtractor()

    while True:
        url = get_url_interactively()
        if url is None:
            print("👋 프로그램을 종료합니다.")
            break

        # 기본 설정으로 처리
        args = argparse.Namespace(metadata=True, save=None, output=None, quiet=False)

        success = process_single_url(extractor, url, args)

        if success:
            # 파일 저장 여부 확인
            if get_user_confirmation("📁 결과를 파일로 저장하시겠습니까?"):
                print("파일 형식을 선택하세요:")
                print("1. 텍스트 파일 (.txt)")
                print("2. JSON 파일 (.json)")

                while True:
                    choice = input("선택 (1-2): ").strip()
                    if choice == "1":
                        args.save = "txt"
                        break
                    elif choice == "2":
                        args.save = "json"
                        break
                    else:
                        print("1 또는 2를 선택해주세요.")

                # 다시 처리 (파일 저장 포함)
                post_data = extractor.get_post_text(url)
                file_path = save_to_file(post_data, None, args.save)
                print_success_message(f"결과를 {file_path}에 저장했습니다.")

        print("\n" + "=" * 60 + "\n")

        if not get_user_confirmation("🔄 다른 게시물을 처리하시겠습니까?"):
            print("👋 프로그램을 종료합니다.")
            break


def main():
    """메인 함수"""
    args = parse_arguments()

    # 배치 파일 처리 모드
    if args.batch_file:
        try:
            # URL 목록 파일 읽기
            urls = read_urls_from_file(args.batch_file)
            print(f"📂 파일에서 {len(urls)}개 URL을 읽었습니다: {args.batch_file}")

            # Instagram 텍스트 추출기 생성
            extractor = InstagramTextExtractor()

            # 배치 처리 실행
            results = process_batch_urls(extractor, urls, args)

            # 통합 결과 저장
            if args.combined_output and results:
                output_format = args.save or 'txt'
                combined_file = save_combined_results(results, output_format)
                print(f"📄 통합 결과 저장: {combined_file}")

            # 성공률에 따른 종료 코드
            success_rate = len(results) / len(urls) if urls else 0
            exit_code = 0 if success_rate >= 0.5 else 1  # 50% 이상 성공시 정상 종료
            sys.exit(exit_code)

        except (FileNotFoundError, ValueError) as e:
            print(f"❌ 배치 파일 처리 오류: {str(e)}")
            sys.exit(1)

    # URL이 제공되지 않은 경우 대화형 모드
    elif not args.url:
        interactive_mode()
        return

    # 명령줄 모드 (단일 URL)
    else:
        extractor = InstagramTextExtractor()
        success = process_single_url(extractor, args.url, args)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 프로그램 실행 중 오류 발생: {str(e)}")
        sys.exit(1)
