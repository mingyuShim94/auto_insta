#!/usr/bin/env python3
"""
FastAPI 서버 실행 스크립트
uv run으로 실행하기 위한 간편 스크립트
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src", "api"]
    )