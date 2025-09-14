# 빠른 시작 가이드

## 🚀 5분만에 시작하기

### 1단계: 실행
```bash
PYTHONPATH=. ./.venv/bin/python -m src
```

### 2단계: URL 입력
```
📱 Instagram URL: https://www.instagram.com/p/DOiSOJwEvAT/
```

### 3단계: 결과 확인
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

## 📋 자주 사용하는 명령어

### 본문만 빠르게 추출
```bash
PYTHONPATH=. ./.venv/bin/python -m src [URL] --quiet
```

### 파일로 저장
```bash
PYTHONPATH=. ./.venv/bin/python -m src [URL] --save txt
```

### 상세 정보 + JSON 저장
```bash
PYTHONPATH=. ./.venv/bin/python -m src [URL] --metadata --save json
```

### 배치 처리 (여러 URL 한번에) ⭐ **NEW**
```bash
# URL 목록 파일 생성
echo "https://www.instagram.com/p/DOiSOJwEvAT/" > urls.txt
echo "https://www.instagram.com/p/DOgZA3hEjQ5/" >> urls.txt

# 배치 처리 실행
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata --save txt --combined-output
```

## ❗ 자주 묻는 질문

**Q: 프로그램이 실행되지 않아요**
A: `PYTHONPATH=.`를 반드시 포함해서 실행하세요.

**Q: 비공개 계정 게시물을 볼 수 없나요?**
A: 현재 버전은 공개 게시물만 지원합니다.

**Q: 어떤 URL 형식을 지원하나요?**
A: `/p/`, `/reel/`, `/tv/` 경로의 Instagram URL을 지원합니다.

---
더 자세한 사용법은 [사용법.md](./사용법.md)를 참고하세요.