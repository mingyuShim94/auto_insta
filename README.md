# Instagram 게시물 텍스트 추출기

Instagram 게시물 링크에서 본문 텍스트를 추출하는 Python CLI 도구입니다.

## 🚀 주요 기능

- **간단한 텍스트 추출**: Instagram 게시물 URL을 입력하면 본문 텍스트를 추출합니다
- **메타데이터 지원**: 작성자, 좋아요 수, 게시 날짜 등 추가 정보 제공
- **다양한 출력 형식**: 콘솔 출력, 텍스트 파일, JSON 파일 저장 지원
- **대화형 모드**: CLI를 통한 사용자 친화적 인터페이스
- **에러 처리**: 다양한 예외 상황에 대한 명확한 안내 메시지

## 📦 설치

### 필수 요구사항

- Python 3.7 이상
- pip (Python 패키지 관리자)

### 설치 단계

1. **저장소 클론**
```bash
git clone <repository-url>
cd auto_insta
```

2. **가상환경 생성 및 활성화**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\\Scripts\\activate  # Windows
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **개발 도구 설치 (선택사항)**
```bash
pip install -r requirements-dev.txt
```

## 🔧 사용법

### 기본 사용법

```bash
# 대화형 모드 (URL이 없으면 자동으로 대화형 모드 실행)
python src/main.py

# 직접 URL 지정
python src/main.py https://www.instagram.com/p/ABC123/
```

### 고급 옵션

```bash
# 메타데이터 포함하여 출력
python src/main.py https://www.instagram.com/p/ABC123/ --metadata

# 결과를 텍스트 파일로 저장
python src/main.py https://www.instagram.com/p/ABC123/ --save txt

# 결과를 JSON 파일로 저장
python src/main.py https://www.instagram.com/p/ABC123/ --save json --output my_post

# 간단한 출력 (본문만)
python src/main.py https://www.instagram.com/p/ABC123/ --quiet

# 모든 옵션 조합
python src/main.py https://www.instagram.com/p/ABC123/ --metadata --save json --output result
```

### 명령줄 옵션

| 옵션 | 단축형 | 설명 |
|------|--------|------|
| `--metadata` | `-m` | 메타데이터 포함 (작성자, 좋아요 수, 날짜 등) |
| `--save FORMAT` | `-s` | 파일로 저장 (`txt` 또는 `json`) |
| `--output FILENAME` | `-o` | 저장할 파일명 (확장자 제외) |
| `--quiet` | `-q` | 최소한의 출력만 표시 |
| `--help` | `-h` | 도움말 표시 |

## 💡 사용 예시

### 1. 대화형 모드

```bash
$ python src/main.py

🎯 Instagram 게시물 텍스트 추출기
----------------------------------------
Instagram 게시물 링크를 입력하세요.
(종료하려면 'quit' 또는 'exit' 입력)

📱 Instagram URL: https://www.instagram.com/p/ABC123/

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

📁 결과를 파일로 저장하시겠습니까? (y/n): y
파일 형식을 선택하세요:
1. 텍스트 파일 (.txt)
2. JSON 파일 (.json)
선택 (1-2): 1

✅ 결과를 outputs/instagram_example_user_20230615_143000.txt에 저장했습니다.
```

### 2. 명령줄 모드

```bash
$ python src/main.py https://www.instagram.com/p/ABC123/ --metadata --save json

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

✅ 결과를 outputs/instagram_example_user_20230615_143000.json에 저장했습니다.
```

### 3. Quiet 모드

```bash
$ python src/main.py https://www.instagram.com/p/ABC123/ --quiet

아름다운 하루입니다! ☀️ #좋은날씨 #인스타그램 #일상
```

## 📁 프로젝트 구조

```
auto_insta/
├── src/                          # 소스 코드
│   ├── __init__.py
│   ├── main.py                   # CLI 진입점
│   ├── extractor.py              # Instagram 텍스트 추출 로직
│   └── utils.py                  # 유틸리티 함수들
├── tests/                        # 테스트 코드
│   ├── __init__.py
│   ├── test_extractor.py
│   ├── test_utils.py
│   └── test_main.py
├── outputs/                      # 저장된 결과 파일들 (자동 생성)
├── requirements.txt              # 프로덕션 의존성
├── requirements-dev.txt          # 개발 의존성
├── README.md
└── CLAUDE.md                     # Claude Code 설정
```

## 🧪 테스트

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 테스트 실행
pytest --cov=src tests/

# 특정 테스트 파일 실행
pytest tests/test_extractor.py

# 상세 출력
pytest -v
```

### 코드 품질 검사

```bash
# 코드 포맷팅 (Black)
black src/ tests/

# 린팅 (Flake8)
flake8 src/ tests/

# 타입 검사 (mypy)
mypy src/
```

## 🚨 에러 처리

프로그램은 다음과 같은 상황들을 적절히 처리합니다:

### URL 관련 오류
- 잘못된 URL 형식
- 존재하지 않는 게시물
- 삭제된 게시물

### 권한 관련 오류
- 비공개 계정의 게시물
- 로그인이 필요한 컨텐츠

### 네트워크 관련 오류
- 인터넷 연결 문제
- Instagram 서버 응답 지연
- Rate limiting (요청 제한)

### 사용 예시

```bash
$ python src/main.py https://invalid-url

🔗 오류 발생:
   유효하지 않은 Instagram URL입니다.

$ python src/main.py https://www.instagram.com/p/PRIVATE/

🔒 오류 발생:
   비공개 계정입니다. 로그인이 필요합니다.
```

## 🔒 제한사항

- **공개 게시물만 지원**: 현재 버전은 로그인 기능을 지원하지 않으므로 공개 게시물만 처리할 수 있습니다
- **Rate Limiting**: Instagram의 요청 제한으로 인해 단시간 내 대량 요청 시 일시적으로 차단될 수 있습니다
- **지원 URL 형식**: `/p/`, `/reel/`, `/tv/` 경로의 게시물만 지원합니다

## 📚 기술 스택

- **Python 3.7+**: 메인 프로그래밍 언어
- **instaloader**: Instagram 데이터 추출 라이브러리
- **argparse**: 명령줄 인수 파싱
- **pytest**: 테스트 프레임워크
- **black**: 코드 포맷팅
- **flake8**: 코드 린팅
- **mypy**: 정적 타입 검사

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 개발 가이드

### 개발 환경 설정

```bash
# 개발 도구 설치
pip install -r requirements-dev.txt

# pre-commit 훅 설정 (선택사항)
pre-commit install
```

### 코드 스타일

- **Black**: 코드 포맷팅
- **Flake8**: PEP 8 준수 검사
- **mypy**: 타입 힌트 검사
- **pytest**: 테스트 작성

### 새로운 기능 추가

1. `src/` 디렉토리에 구현
2. `tests/` 디렉토리에 테스트 추가
3. 문서 업데이트
4. 모든 테스트 통과 확인

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## ⚠️ 면책 조항

이 도구는 Instagram과 공식적으로 관련이 없는 독립적인 프로젝트입니다. Instagram의 서비스 약관을 준수하여 사용하시기 바랍니다. 개인적인 용도로만 사용하시고, 상업적 목적이나 대량 데이터 수집에는 사용하지 마세요.

---

**문제가 발생하거나 개선 사항이 있으시면 Issue를 통해 알려주세요!** 🚀