# 사용 예시 모음

## 📋 목차
1. [기본 사용 예시](#기본-사용-예시)
2. [실제 테스트 결과](#실제-테스트-결과)
3. [파일 저장 예시](#파일-저장-예시)
4. [배치 처리 예시](#배치-처리-예시) ⭐ **NEW**
5. [에러 상황 예시](#에러-상황-예시)
6. [대화형 배치 처리 워크플로우](#대화형-배치-처리-워크플로우)

## 기본 사용 예시

### 예시 1: 간단한 텍스트 추출
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/ABC123/ --quiet

아름다운 하루입니다! ☀️ #좋은날씨 #인스타그램 #일상
```

### 예시 2: 메타데이터 포함 출력
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/ABC123/ --metadata

📥 게시물 정보를 가져오는 중...

============================================================
📱 Instagram 게시물 본문
============================================================
👤 작성자: @example_user
❤️ 좋아요: 1,234개
📅 게시일: 2023년 06월 15일 14:30
📎 미디어: 📸 이미지
------------------------------------------------------------
💬 본문:
아름다운 하루입니다! ☀️ #좋은날씨 #인스타그램 #일상
============================================================
```

### 예시 3: 대화형 모드
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src

🎯 Instagram 게시물 텍스트 추출기
----------------------------------------
Instagram 게시물 링크를 입력하세요.
(종료하려면 'quit' 또는 'exit' 입력)

📱 Instagram URL: https://www.instagram.com/p/ABC123/

📥 게시물 정보를 가져오는 중...
[결과 출력...]

📁 결과를 파일로 저장하시겠습니까? (y/n): y
파일 형식을 선택하세요:
1. 텍스트 파일 (.txt)
2. JSON 파일 (.json)
선택 (1-2): 1

✅ 결과를 outputs/instagram_example_user_20230615_143000.txt에 저장했습니다.

============================================================

🔄 다른 게시물을 처리하시겠습니까? (y/n): n
👋 프로그램을 종료합니다.
```

## 실제 테스트 결과

### 테스트 URL: https://www.instagram.com/p/DOiSOJwEvAT/

**명령어:**
```bash
PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/DOiSOJwEvAT/ --metadata
```

**실행 결과:**
```
📥 게시물 정보를 가져오는 중...
============================================================
📱 Instagram 게시물 본문
============================================================
👤 작성자: @theallmy
❤️ 좋아요: 14개
📅 게시일: 2025년 09월 13일 08:27
📎 미디어: 📸 이미지
------------------------------------------------------------
💬 본문:
예쁜 아이들. 🥰 진짜 이 일을 하면서 계속 준비했던 이야기 역사특강 과연 잘 할 수 있을까? 우리 아이들이 역사의 흐름을 쉽게 그리고 정확하게 알 수 있는 기회를 마련하고 싶었다. 그리고 냅다 공지해버렸다. 자면서도 강의를 했다. 드뎌 오늘. 비가 온다. 아이들이 이 비를 맞으며 몇 명이나 올까? 그래, 오는 아이들 위해 열심히 해보자. 찡~~~~ 감동🥹 처음에 떨리는 내 목소리가 나한테 크게 들렸다. 초롱초롱~ 이 아이들에게 보답해야지~ 끝나고 나가는데 아이들이 재미 있었다고 한다. 문자로 재미 있었다는 아이들 메시지를 전달해 주시는 학부모님들~ 감사합니다.☺️ 조선 왕들에 대해서도 열심히 준비할게요🥰 #초등보습학원 #초등특강 #초등전과목✍️ #한국사특강 #여기는부산 #명지국제신도
============================================================
```

**특징:**
- ✅ 한글 텍스트 완벽 추출
- ✅ 이모지 정상 표시 (🥰🥹☺️✍️)
- ✅ 해시태그 포함
- ✅ 긴 텍스트 처리
- ✅ 메타데이터 정확히 추출

## 파일 저장 예시

### TXT 파일 저장
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/DOiSOJwEvAT/ --save txt --output my_post

📥 게시물 정보를 가져오는 중...
[결과 출력...]

✅ 결과를 outputs/my_post.txt에 저장했습니다.
```

**저장된 파일 내용 (outputs/my_post.txt):**
```
============================================================
📱 Instagram 게시물 본문
============================================================
👤 작성자: @theallmy
❤️ 좋아요: 14개
📅 게시일: 2025년 09월 13일 08:27
📎 미디어: 📸 이미지
------------------------------------------------------------
💬 본문:
예쁜 아이들. 🥰 진짜 이 일을 하면서 계속 준비했던...
============================================================
```

### JSON 파일 저장
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/DOiSOJwEvAT/ --save json --output data

📥 게시물 정보를 가져오는 중...
[결과 출력...]

✅ 결과를 outputs/data.json에 저장했습니다.
```

**저장된 파일 내용 (outputs/data.json):**
```json
{
  "text": "예쁜 아이들. 🥰 진짜 이 일을 하면서 계속 준비했던 이야기 역사특강 과연 잘 할 수 있을까?...",
  "username": "theallmy",
  "likes": 14,
  "date": "2025-09-13T08:27:00",
  "media_count": 1,
  "is_video": false,
  "url": "https://www.instagram.com/p/DOiSOJwEvAT/"
}
```

## 배치 처리 예시 ⭐ **NEW**

### 예시 1: 기본 배치 처리

**URL 목록 파일 준비 (urls.txt):**
```
https://www.instagram.com/p/DOgZA3hEjQ5/
https://www.instagram.com/p/DOiSOJwEvAT/
https://www.instagram.com/p/DN3NOXpZENJ/
https://www.instagram.com/p/DOSS3O8kh5I/
```

**명령어:**
```bash
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata
```

**실행 결과:**
```
📥 배치 처리를 시작합니다...
📊 총 4개의 URL을 처리합니다.

🔄 처리 중... [1/4] https://www.instagram.com/p/DOgZA3hEjQ5/
✅ 성공: @theallmy (10 좋아요)

⏳ 3초 대기 중...

🔄 처리 중... [2/4] https://www.instagram.com/p/DOiSOJwEvAT/
✅ 성공: @theallmy (14 좋아요)

⏳ 3초 대기 중...

🔄 처리 중... [3/4] https://www.instagram.com/p/DN3NOXpZENJ/
✅ 성공: @theallmy (19 좋아요)

⏳ 3초 대기 중...

🔄 처리 중... [4/4] https://www.instagram.com/p/DOSS3O8kh5I/
✅ 성공: @wealbuza (7 좋아요)

📊 배치 처리 완료!
✅ 성공: 4개
❌ 실패: 0개
📁 저장된 파일: outputs/ 디렉토리 확인
```

### 예시 2: 통합 TXT 파일로 저장

**명령어:**
```bash
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata --save txt --combined-output
```

**저장된 파일 (outputs/instagram_batch_combined_20250915_001347.txt):**
```
================================================================================
📱 Instagram 배치 처리 결과
📅 처리일시: 2025년 09월 15일 00:13:47
📊 총 처리 건수: 4개
================================================================================

[01] https://www.instagram.com/p/DOgZA3hEjQ5/
👤 작성자: @theallmy
❤️ 좋아요: 10개
📅 게시일: 2025년 09월 12일 14:48

💬 본문:
벼락치기 내일은 역사특강 storytelling 간략하게 정리라도 해야 하는데...

------------------------------------------------------------

[02] https://www.instagram.com/p/DOiSOJwEvAT/
👤 작성자: @theallmy
❤️ 좋아요: 14개
📅 게시일: 2025년 09월 13일 08:27

💬 본문:
예쁜 아이들. 🥰 진짜 이 일을 하면서 계속 준비했던 이야기...

------------------------------------------------------------
```

### 예시 3: 통합 JSON 파일로 저장

**명령어:**
```bash
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata --save json --combined-output
```

**저장된 파일 (outputs/instagram_batch_combined_20250915_001238.json):**
```json
{
  "processed_at": "2025-09-15T00:12:38.386876",
  "total_count": 4,
  "results": [
    {
      "text": "벼락치기 내일은 역사특강 storytelling...",
      "username": "theallmy",
      "likes": 10,
      "date": "2025-09-12T14:48:29",
      "media_count": 1,
      "is_video": false,
      "url": "https://www.instagram.com/p/DOgZA3hEjQ5/"
    },
    {
      "text": "예쁜 아이들. 🥰 진짜 이 일을 하면서...",
      "username": "theallmy",
      "likes": 14,
      "date": "2025-09-13T08:27:37",
      "media_count": 1,
      "is_video": false,
      "url": "https://www.instagram.com/p/DOiSOJwEvAT/"
    }
  ]
}
```

### 예시 4: 처리 간격 조정

**명령어 (5초 간격으로 처리):**
```bash
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata --delay 5
```

**실행 결과:**
```
📥 배치 처리를 시작합니다...
📊 총 4개의 URL을 처리합니다.

🔄 처리 중... [1/4] https://www.instagram.com/p/DOgZA3hEjQ5/
✅ 성공: @theallmy (10 좋아요)

⏳ 5초 대기 중...

🔄 처리 중... [2/4] https://www.instagram.com/p/DOiSOJwEvAT/
✅ 성공: @theallmy (14 좋아요)
...
```

### 예시 5: 에러가 있는 배치 처리

**URL 목록 파일 (mixed_urls.txt):**
```
https://www.instagram.com/p/DOiSOJwEvAT/  # 정상 URL
https://www.instagram.com/p/NOTEXIST/      # 존재하지 않는 게시물
https://www.instagram.com/p/DN3NOXpZENJ/  # 정상 URL
```

**실행 결과:**
```
📥 배치 처리를 시작합니다...
📊 총 3개의 URL을 처리합니다.

🔄 처리 중... [1/3] https://www.instagram.com/p/DOiSOJwEvAT/
✅ 성공: @theallmy (14 좋아요)

⏳ 3초 대기 중...

🔄 처리 중... [2/3] https://www.instagram.com/p/NOTEXIST/
❌ 실패: 게시물이 삭제되었거나 존재하지 않습니다.

⏳ 3초 대기 중...

🔄 처리 중... [3/3] https://www.instagram.com/p/DN3NOXpZENJ/
✅ 성공: @theallmy (19 좋아요)

📊 배치 처리 완료!
✅ 성공: 2개
❌ 실패: 1개
📁 저장된 파일: outputs/ 디렉토리 확인
```

## 에러 상황 예시

### 1. 잘못된 URL 형식
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://facebook.com/post/123

🔗 오류 발생:
   유효하지 않은 Instagram URL입니다.
```

### 2. 존재하지 않는 게시물
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/NOTEXIST/

📥 게시물 정보를 가져오는 중...

🔗 오류 발생:
   게시물이 삭제되었거나 존재하지 않습니다.
```

### 3. 비공개 계정 게시물
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/PRIVATE123/

📥 게시물 정보를 가져오는 중...

🔒 오류 발생:
   비공개 계정입니다. 로그인이 필요합니다.
```

### 4. 네트워크 연결 오류
```bash
$ PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/ABC123/

📥 게시물 정보를 가져오는 중...

🌐 오류 발생:
   네트워크 연결 오류: Connection timeout
```

## 대화형 배치 처리 워크플로우

### 시나리오: 여러 게시물을 대화형 모드에서 연속 처리

```bash
$ PYTHONPATH=. ./.venv/bin/python -m src

🎯 Instagram 게시물 텍스트 추출기
----------------------------------------
Instagram 게시물 링크를 입력하세요.
(종료하려면 'quit' 또는 'exit' 입력)

# 첫 번째 게시물
📱 Instagram URL: https://www.instagram.com/p/ABC123/
[처리 및 결과 출력]
📁 결과를 파일로 저장하시겠습니까? (y/n): y
파일 형식을 선택하세요:
1. 텍스트 파일 (.txt)
2. JSON 파일 (.json)
선택 (1-2): 2
✅ 결과를 outputs/instagram_user1_20230615_100000.json에 저장했습니다.

============================================================

🔄 다른 게시물을 처리하시겠습니까? (y/n): y

# 두 번째 게시물
📱 Instagram URL: https://www.instagram.com/p/XYZ789/
[처리 및 결과 출력]
📁 결과를 파일로 저장하시겠습니까? (y/n): y
선택 (1-2): 2
✅ 결과를 outputs/instagram_user2_20230615_100130.json에 저장했습니다.

============================================================

🔄 다른 게시물을 처리하시겠습니까? (y/n): n
👋 프로그램을 종료합니다.
```

### 처리 후 파일 확인
```bash
$ ls -la outputs/
drwxr-xr-x  4 user  group   128 Sep 15 10:01 .
drwxr-xr-x  8 user  group   256 Sep 15 10:00 ..
-rw-r--r--  1 user  group   543 Sep 15 10:00 instagram_user1_20230615_100000.json
-rw-r--r--  1 user  group   612 Sep 15 10:01 instagram_user2_20230615_100130.json
```

## 고급 사용 패턴

### 파이프라인 처리
```bash
# 조용한 모드로 텍스트만 추출하여 다른 프로그램으로 전달
PYTHONPATH=. ./.venv/bin/python -m src [URL] --quiet | grep "#" | wc -l
# 결과: 해시태그 개수 출력
```

### 자동화 스크립트 vs 배치 처리 비교

**기존 스크립트 방식:**
```bash
#!/bin/bash
# 수동으로 구현한 배치 처리 (비추천)

while IFS= read -r url; do
    echo "Processing: $url"
    PYTHONPATH=. ./.venv/bin/python -m src "$url" --save json --quiet
    sleep 2
done < urls.txt
```

**새로운 내장 배치 처리 (권장):**
```bash
# 내장 배치 처리 기능 사용
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --save json --combined-output --delay 2
```

**배치 처리 장점:**
- ✅ 진행상황 실시간 표시
- ✅ 에러 처리 및 복구
- ✅ 통합 결과 파일 옵션
- ✅ 자동 파일명 생성
- ✅ Rate limiting 자동 관리

## 성능 참고사항

### 처리 시간
- 일반적인 게시물: 2-5초
- 긴 텍스트가 있는 게시물: 3-7초
- 네트워크 상태에 따라 변동 가능

### 권장 사용량
- 연속 처리 시 요청 간 2-3초 간격 권장
- 시간당 50개 이하 게시물 처리 권장
- Rate limiting 발생 시 10-15분 대기 후 재시도