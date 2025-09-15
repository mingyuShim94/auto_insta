#!/bin/bash
# Instagram 배치 처리 간편 실행 스크립트
# 사용법: ./run_batch.sh

echo "🚀 Instagram 배치 처리 시작..."
echo "📂 파일: urls.txt"
echo "💾 출력: JSON 형식, 통합 파일"
echo ""

PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata --save json --combined-output

echo ""
echo "✅ 배치 처리 완료!"
echo "📄 결과 파일이 outputs/ 디렉토리에 저장되었습니다."