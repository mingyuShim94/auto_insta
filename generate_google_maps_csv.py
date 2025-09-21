#!/usr/bin/env python3
"""
Google My Maps CSV 생성 스크립트
장소 정보가 담긴 JSON 파일을 Google My Maps에서 가져올 수 있는 CSV 형식으로 변환
"""

import json
import csv
import sys
from pathlib import Path


def load_locations_data(json_file_path):
    """JSON 파일에서 장소 데이터를 로드"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('locations', [])
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {json_file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return []


def generate_csv(locations, output_file_path):
    """장소 데이터를 Google My Maps 호환 CSV로 변환"""

    # Google My Maps에서 사용할 CSV 헤더
    headers = [
        'Name',           # 장소명 (필수)
        'Address',        # 주소 (필수)
        'Description',    # 설명
        'Category',       # 카테고리
        'Website',        # 웹사이트 URL
        'Likes',          # 좋아요 수
        'Rating',         # 평점
        'Price'           # 가격대
    ]

    try:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # 헤더 작성
            writer.writerow(headers)

            # 각 장소 데이터 작성
            for location in locations:
                # 장소명 (한국어 우선, 영어 백업)
                name = location.get('name', location.get('name_en', ''))

                # 주소
                address = location.get('address', '')

                # 설명
                description = location.get('description', '')

                # 카테고리
                category = location.get('category', '')

                # 웹사이트
                website = location.get('website', '')

                # 좋아요 수
                likes = location.get('likes', 0)

                # 평점
                rating = location.get('rating', '')

                # 가격대
                price_range = location.get('price_range', '')

                # CSV 행 작성
                writer.writerow([
                    name,
                    address,
                    description,
                    category,
                    website,
                    likes,
                    rating,
                    price_range
                ])

        return True

    except Exception as e:
        print(f"CSV 파일 생성 중 오류 발생: {e}")
        return False


def main():
    """메인 실행 함수"""

    # 입력 파일 및 출력 파일 경로 설정
    input_file = "mock_locations.json"
    output_file = "locations_for_google_maps.csv"

    # 명령행 인수가 있으면 사용
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print(f"입력 파일: {input_file}")
    print(f"출력 파일: {output_file}")

    # 장소 데이터 로드
    locations = load_locations_data(input_file)

    if not locations:
        print("장소 데이터가 없습니다.")
        return

    print(f"총 {len(locations)}개의 장소를 발견했습니다.")

    # CSV 생성
    if generate_csv(locations, output_file):
        print(f"✅ CSV 파일이 성공적으로 생성되었습니다: {output_file}")
        print("\n📋 Google My Maps 업로드 방법:")
        print("1. https://mymaps.google.com 접속")
        print("2. '새 지도 만들기' 클릭")
        print("3. '가져오기' 클릭")
        print(f"4. '{output_file}' 파일 업로드")
        print("5. 컬럼 매핑 확인 후 완료")

        # 생성된 데이터 미리보기
        print(f"\n📍 생성된 장소 목록:")
        for i, location in enumerate(locations, 1):
            name = location.get('name', location.get('name_en', ''))
            category = location.get('category', '')
            print(f"  {i}. {name} ({category})")

    else:
        print("❌ CSV 파일 생성에 실패했습니다.")


if __name__ == "__main__":
    main()