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
	@echo "  make batch-individual - 개별 JSON 파일로 저장"
	@echo "  make clean          - 출력 디렉토리 정리"
	@echo "  make help           - 도움말 표시"

.PHONY: batch batch-txt batch-individual clean help