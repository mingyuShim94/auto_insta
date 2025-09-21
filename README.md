# Instagram Text Extractor

Instagram 게시물 링크에서 텍스트를 추출하는 풀스택 프로젝트입니다.

## 프로젝트 구성

### 📱 Flutter App
모바일 앱으로 Instagram URL을 입력하면 텍스트를 추출해주는 사용자 친화적인 인터페이스를 제공합니다.

### 🐍 Python Backend
- **CLI 도구**: 명령줄에서 Instagram 텍스트 추출
- **FastAPI 서버**: REST API로 텍스트 추출 서비스 제공

## 프로젝트 구조

```
auto_insta/
├── flutter_app/         # Flutter 모바일 앱
│   ├── lib/
│   │   ├── models/      # API 응답 모델
│   │   ├── services/    # API 서비스 클래스
│   │   ├── screens/     # UI 화면
│   │   └── main.dart    # 앱 진입점
│   └── pubspec.yaml     # Flutter 의존성
├── src/                 # Python CLI 도구
│   ├── main.py          # CLI 메인 인터페이스
│   ├── extractor.py     # Instagram 텍스트 추출 로직
│   └── utils.py         # 유틸리티 함수들
├── api/                 # FastAPI 서버
│   ├── main.py          # FastAPI 애플리케이션
│   ├── models.py        # Pydantic 모델
│   └── services.py      # 비즈니스 로직
├── outputs/             # CLI 추출 결과 저장
├── pyproject.toml       # Python 프로젝트 설정
├── run_api.py          # FastAPI 서버 실행 스크립트
└── README.md           # 프로젝트 문서
```

## 개발 환경 설정

### Python Backend

#### 1. 의존성 설치
```bash
# uv를 사용한 빠른 설치 (권장)
uv sync

# 또는 개발 의존성 포함
uv sync --dev
```

#### 2. CLI 도구 실행
```bash
# 단일 Instagram URL 처리
uv run python -m src https://www.instagram.com/p/ABC123/

# 메타데이터 포함하여 JSON으로 저장
uv run python -m src https://www.instagram.com/p/ABC123/ --metadata --save json

# 배치 처리 (URL 목록 파일)
uv run python -m src --batch urls.txt
```

#### 3. FastAPI 서버 실행
```bash
# 개발 서버 시작
uv run python run_api.py

# 또는 직접 uvicorn 실행
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. API 테스트
```bash
# 헬스체크
curl http://localhost:8000/health

# 텍스트 추출
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/p/ABC123/"}'

# API 문서 확인: http://localhost:8000/docs
```

### Flutter App

#### 1. Flutter 프로젝트 설정
```bash
cd flutter_app
flutter pub get
```

#### 2. 코드 생성 (JSON 직렬화)
```bash
cd flutter_app
dart run build_runner build
```

#### 3. 앱 실행
```bash
cd flutter_app
flutter run
```

## 사용 방법

### 1. 백엔드 서버 시작
```bash
uv run python run_api.py
```
서버가 `http://localhost:8000`에서 실행됩니다.

### 2. Flutter 앱 실행
```bash
cd flutter_app
flutter run
```

### 3. 앱 사용
1. Instagram 게시물 URL 입력
2. "텍스트 추출" 버튼 클릭
3. 추출된 텍스트 및 메타데이터 확인

## API 엔드포인트

### POST /extract
Instagram URL에서 텍스트 추출

**요청:**
```json
{
  "url": "https://www.instagram.com/p/ABC123/"
}
```

**응답:**
```json
{
  "success": true,
  "data": {
    "text": "추출된 본문 텍스트",
    "username": "작성자명",
    "likes": 1234,
    "date": "2025-01-19T12:00:00",
    "media_count": 1,
    "is_video": false,
    "url": "원본 URL"
  },
  "error": null
}
```

### GET /health
서버 상태 확인

### GET /docs
Swagger UI API 문서

## 개발 도구

### Python 코드 품질
```bash
# 코드 포맷팅
uv run black .

# 린팅
uv run flake8 src/ api/

# 타입 체크
uv run mypy src/ api/

# 테스트
uv run pytest
```

### Flutter 개발
```bash
# 코드 분석
cd flutter_app
flutter analyze

# 테스트
flutter test

# 빌드
flutter build apk  # Android
flutter build ios  # iOS
```

## 기술 스택

- **Backend**: Python 3.13, FastAPI, Instaloader, uv
- **Frontend**: Flutter, Dart, HTTP client
- **API**: REST API with JSON
- **패키지 관리**: uv (Python), pub (Flutter)

## 주요 기능

✅ Instagram 게시물 텍스트 추출  
✅ 사용자명, 좋아요 수, 날짜 등 메타데이터 제공  
✅ 크로스플랫폼 모바일 앱 (iOS/Android)  
✅ REST API 서버  
✅ CLI 도구로 배치 처리 지원  
✅ JSON/텍스트 파일 저장 기능  

## 배포

### Python API 서버
```bash
# 프로덕션 빌드
uv build

# Docker를 사용한 배포 (예정)
# Railway, Render, AWS 등에 배포 가능
```

### Flutter 앱
```bash
cd flutter_app

# Android 빌드
flutter build apk --release

# iOS 빌드 (macOS에서만)
flutter build ios --release
```

## 라이선스

이 프로젝트는 개인 프로젝트입니다.

## 주의사항

- Instagram의 이용약관을 준수하여 사용하세요
- 과도한 요청은 IP 차단을 초래할 수 있습니다
- 비공개 계정의 게시물은 추출할 수 없습니다