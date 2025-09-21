# Instagram 자동 추출기 Makefile

# 기본 변수
PYTHON = PYTHONPATH=. ./.venv/bin/python
BATCH_FILE = urls.txt
OUTPUT_DIR = outputs

# 배치 처리 (기본)
batch:
	@echo "🚀 Instagram 배치 처리 시작..."
	@echo "📂 파일: $(BATCH_FILE)"
	@echo "💾 출력: JSON 형식, 통합 파일"
	@echo ""
	$(PYTHON) -m src --batch-file $(BATCH_FILE) --metadata --save json --combined-output

# 텍스트 형식으로 배치 처리
batch-txt:
	@echo "📝 텍스트 형식으로 배치 처리..."
	$(PYTHON) -m src --batch-file $(BATCH_FILE) --metadata --save txt --combined-output

# 개별 파일로 저장 (통합하지 않음)
batch-individual:
	@echo "📁 개별 파일로 저장..."
	$(PYTHON) -m src --batch-file $(BATCH_FILE) --metadata --save json

# 간단한 모드 (text와 url만)
batch-simple:
	@echo "📝 간단한 모드로 배치 처리..."
	@echo "📂 파일: $(BATCH_FILE)"
	@echo "💾 출력: JSON 형식, text+url만 포함"
	@echo ""
	$(PYTHON) -m src --batch-file $(BATCH_FILE) --save json --simple --combined-output

# 제목 포함 배치 처리
batch-with-titles:
	@echo "📚 제목 포함 배치 처리..."
	@echo "📂 파일: urls_data.txt"
	@echo "💾 출력: JSON 형식, 제목+전체 메타데이터"
	@echo ""
	$(PYTHON) -m src --batch-file urls_data.txt --with-titles --metadata --save json --combined-output

# 제목 포함 간단한 모드
batch-with-titles-simple:
	@echo "📚 제목 포함 간단한 모드..."
	@echo "📂 파일: urls_data.txt"
	@echo "💾 출력: JSON 형식, 제목+text+url만"
	@echo ""
	$(PYTHON) -m src --batch-file urls_data.txt --with-titles --save json --simple --combined-output

# 출력 디렉토리 정리
clean:
	@echo "🧹 출력 디렉토리 정리..."
	rm -rf $(OUTPUT_DIR)/*
	@echo "✅ 정리 완료!"

# 도움말
help:
	@echo "📖 사용 가능한 명령어:"
	@echo "  make batch          - JSON 통합 파일로 배치 처리 (기본)"
	@echo "  make batch-txt      - 텍스트 통합 파일로 배치 처리"
	@echo "  make batch-simple   - 간단한 모드 (text+url만 JSON)"
	@echo "  make batch-with-titles - 제목 포함 전체 모드 (urls_data.txt)"
	@echo "  make batch-with-titles-simple - 제목 포함 간단 모드"
	@echo "  make batch-individual - 개별 JSON 파일로 저장"
	@echo "  make clean          - 출력 디렉토리 정리"
	@echo "  make help           - 도움말 표시"

.PHONY: batch batch-txt batch-simple batch-with-titles batch-with-titles-simple batch-individual clean help