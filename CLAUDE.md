# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Instagram 텍스트 추출 프로젝트 (`auto_insta`) - Instagram 게시물 링크에서 텍스트를 추출하는 CLI 도구와 FastAPI 웹 서버를 제공합니다.

## Development Environment

### Python Setup
- **Python Version**: 3.13.7 (installed via Homebrew)
- **Package Manager**: uv (빠른 Python 패키지 매니저)
- **Virtual Environment**: `.venv/` (uv로 자동 관리)
- **Project Configuration**: `pyproject.toml`

### Environment Setup
```bash
# 의존성 설치 및 가상환경 구성
uv sync

# 개발 의존성 포함 설치
uv sync --dev
```

## Application Commands

### CLI 도구 실행
```bash
# 단일 Instagram URL 처리
uv run python -m src https://www.instagram.com/p/ABC123/

# 배치 처리 (파일에서 URL 목록 읽기)
uv run python -m src --batch urls.txt

# 메타데이터 포함하여 JSON으로 저장
uv run python -m src https://www.instagram.com/p/ABC123/ --metadata --save json
```

### FastAPI 서버 실행
```bash
# 개발 서버 실행 (추천)
uv run python run_api.py

# 또는 직접 uvicorn 실행
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### API 사용 예시
```bash
# 헬스체크
curl http://localhost:8000/health

# 텍스트 추출
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/p/ABC123/"}'

# API 문서 확인
# 브라우저에서 http://localhost:8000/docs 접속
```

## Code Quality Commands

### Formatting
```bash
# Format all Python files
uv run black .

# Format specific file
uv run black src/main.py
```

### Linting
```bash
# Check code style
uv run flake8 src/ api/
```

### Type Checking
```bash
# Check type hints
uv run mypy src/ api/
```

### Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov=api tests/
```

## Project Structure

```
auto_insta/
├── .venv/                # Virtual environment (uv로 자동 관리)
├── src/                  # Instagram 텍스트 추출 CLI 도구
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py          # CLI 메인 인터페이스
│   ├── extractor.py     # Instagram 텍스트 추출 로직
│   └── utils.py         # 유틸리티 함수들
├── api/                  # FastAPI 웹 서버
│   ├── __init__.py
│   ├── main.py          # FastAPI 애플리케이션
│   ├── models.py        # Pydantic 모델 정의
│   └── services.py      # 비즈니스 로직 서비스
├── tests/                # 테스트 코드
│   └── test_*.py
├── outputs/              # 추출 결과 저장 디렉토리
├── pyproject.toml        # 프로젝트 설정 및 의존성
├── uv.lock              # 의존성 잠금 파일
├── run_api.py           # FastAPI 서버 실행 스크립트
├── requirements.txt      # 기존 의존성 (레거시)
├── requirements-api.txt  # 기존 API 의존성 (레거시)
└── CLAUDE.md            # 개발 가이드
```

## Dependency Management

### uv 사용 (권장)
```bash
# 새 의존성 추가
uv add package_name

# 개발 의존성 추가
uv add --dev package_name

# 의존성 제거
uv remove package_name

# 환경 동기화
uv sync
```

## VS Code Configuration

`.vscode/settings.json` 권장 설정:
```json
{
    "python.interpreter.path": "./.venv/bin/python",
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

## Important Notes

- **Package Manager**: uv 사용으로 빠른 의존성 관리
- **Python Version**: 3.13.7 (최신 안정 버전)
- **Project Type**: Instagram 텍스트 추출 CLI + FastAPI 서버
- **Development**: pyproject.toml 기반 현대적 Python 프로젝트 구조
- **API Documentation**: 서버 실행 후 `/docs` 경로에서 Swagger UI 확인 가능