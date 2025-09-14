# 문제 해결 가이드

## 📋 목차
1. [실행 관련 문제](#실행-관련-문제)
2. [네트워크 관련 문제](#네트워크-관련-문제)
3. [URL 관련 문제](#url-관련-문제)
4. [파일 저장 관련 문제](#파일-저장-관련-문제)
5. [배치 처리 관련 문제](#배치-처리-관련-문제) ⭐ **NEW**
6. [성능 관련 문제](#성능-관련-문제)
7. [일반적인 해결책](#일반적인-해결책)

## 실행 관련 문제

### ❌ "No module named 'src'" 오류

**증상:**
```
ModuleNotFoundError: No module named 'src'
```

**원인:** PYTHONPATH가 설정되지 않음

**해결책:**
```bash
# 올바른 실행 방법
PYTHONPATH=. ./.venv/bin/python -m src [URL]

# 또는 프로젝트 루트 디렉토리에서 실행하는지 확인
pwd
# 결과: /Users/username/auto_insta 와 같은 프로젝트 루트 경로여야 함
```

### ❌ "command not found: python" 오류

**증상:**
```
bash: ./.venv/bin/python: No such file or directory
```

**원인:** 가상환경이 제대로 설치되지 않음

**해결책:**
```bash
# 가상환경 재생성
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 또는 직접 Python 경로 확인
which python3
# 해당 경로로 실행
```

### ❌ 권한 관련 오류

**증상:**
```
Permission denied: ./.venv/bin/python
```

**해결책:**
```bash
# 실행 권한 부여
chmod +x .venv/bin/python

# 또는 시스템 Python 사용
python3 -m pip install --user instaloader
python3 -m src [URL]
```

## 네트워크 관련 문제

### 🌐 "네트워크 연결 오류" 메시지

**증상:**
```
🌐 오류 발생:
   네트워크 연결 오류: Connection timeout
```

**해결책:**
1. **인터넷 연결 확인**
   ```bash
   ping instagram.com
   curl -I https://instagram.com
   ```

2. **방화벽/프록시 확인**
   ```bash
   # 프록시 설정 확인
   echo $HTTP_PROXY
   echo $HTTPS_PROXY

   # 프록시 해제 후 재시도
   unset HTTP_PROXY HTTPS_PROXY
   ```

3. **DNS 문제 해결**
   ```bash
   # DNS 초기화 (macOS)
   sudo dscacheutil -flushcache

   # 다른 DNS 서버 시도
   # Google DNS: 8.8.8.8, 8.8.4.4
   ```

### 🚫 "403 Forbidden" 오류

**증상:**
```
JSON Query to graphql/query: 403 Forbidden when accessing https://www.instagram.com/graphql/query [retrying; skip with ^C]
```

**원인:** Instagram의 Rate Limiting 또는 차단

**해결책:**
1. **대기 후 재시도**
   ```bash
   # 15-30분 대기 후 재시도
   sleep 900  # 15분 대기
   ```

2. **VPN 사용 중이면 해제**
   ```bash
   # VPN 연결 해제 후 재시도
   ```

3. **User-Agent 확인**
   - 프로그램 내장 User-Agent가 자동으로 설정됨
   - 대부분의 경우 핵심 데이터는 추출 성공

## URL 관련 문제

### 🔗 "유효하지 않은 Instagram URL" 오류

**증상:**
```
🔗 오류 발생:
   유효하지 않은 Instagram URL입니다.
```

**지원되는 URL 형식:**
```bash
✅ 올바른 형식:
https://www.instagram.com/p/ABC123/
https://instagram.com/p/ABC123/
https://www.instagram.com/reel/ABC123/
https://instagram.com/tv/ABC123/

❌ 잘못된 형식:
https://www.instagram.com/username/
https://www.instagram.com/
https://facebook.com/post/123
instagram.com/p/ABC123  # http:// 또는 https:// 누락
```

**해결책:**
1. **URL 형식 확인**
   ```bash
   # Instagram 앱에서 "링크 복사" 사용
   # 브라우저 주소창에서 전체 URL 복사
   ```

2. **URL 인코딩 문제**
   ```bash
   # URL에 특수문자가 있으면 따옴표로 감싸기
   PYTHONPATH=. ./.venv/bin/python -m src "https://www.instagram.com/p/ABC123/?utm_source=ig_web_copy_link"
   ```

### 🔗 "게시물이 삭제되었거나 존재하지 않습니다" 오류

**원인:**
- 게시물이 실제로 삭제됨
- URL의 shortcode가 잘못됨
- 일시적인 Instagram 서버 오류

**해결책:**
1. **URL 재확인**
   ```bash
   # 브라우저에서 해당 URL이 정상적으로 열리는지 확인
   ```

2. **잠시 후 재시도**
   ```bash
   # 1-2분 후 다시 실행
   ```

## 파일 저장 관련 문제

### 📁 "파일을 저장할 수 없습니다" 오류

**원인:** 권한 문제 또는 디스크 공간 부족

**해결책:**
1. **권한 확인**
   ```bash
   # outputs 디렉토리 권한 확인
   ls -la outputs/

   # 권한 수정
   chmod 755 outputs/
   ```

2. **디스크 공간 확인**
   ```bash
   # 디스크 공간 확인
   df -h

   # 불필요한 파일 정리
   rm outputs/old_file.txt
   ```

3. **수동 디렉토리 생성**
   ```bash
   mkdir -p outputs
   ```

### 📄 파일 내용이 깨짐

**증상:** 한글이나 이모지가 깨져서 저장됨

**원인:** 인코딩 문제

**해결책:**
```bash
# UTF-8 인코딩으로 파일 열기 (macOS)
open -a TextEdit outputs/filename.txt

# 인코딩 확인
file -I outputs/filename.txt

# 올바른 인코딩으로 변환
iconv -f UTF-8 -t UTF-8 outputs/filename.txt
```

## 배치 처리 관련 문제 ⭐ **NEW**

### 📄 "URL 목록 파일을 읽을 수 없습니다" 오류

**증상:**
```
❌ 오류 발생: URL 목록 파일을 읽을 수 없습니다.
```

**원인:**
- 파일이 존재하지 않음
- 파일 권한 문제
- 잘못된 파일 경로

**해결책:**
```bash
# 1. 파일 존재 확인
ls -la urls.txt

# 2. 파일 생성
cat > urls.txt << EOF
https://www.instagram.com/p/DOiSOJwEvAT/
https://www.instagram.com/p/DOgZA3hEjQ5/
EOF

# 3. 권한 확인
chmod 644 urls.txt

# 4. 절대 경로 사용
PYTHONPATH=. ./.venv/bin/python -m src --batch-file /full/path/to/urls.txt
```

### 📝 "URL 목록 파일이 비어있습니다" 오류

**증상:**
```
⚠️  경고: URL 목록 파일이 비어있습니다.
```

**원인:**
- 파일에 유효한 URL이 없음
- 모든 줄이 주석 처리됨
- 빈 줄만 존재

**해결책:**
```bash
# 1. 파일 내용 확인
cat -n urls.txt

# 2. 올바른 형식 확인
# ✅ 올바른 형식:
https://www.instagram.com/p/ABC123/
# 이것은 주석입니다
https://www.instagram.com/p/XYZ789/

# ❌ 잘못된 형식:
# https://www.instagram.com/p/ABC123/  (모두 주석)

# 3. 빈 줄 및 주석 제거 후 확인
grep -v '^#' urls.txt | grep -v '^$'
```

### 🚫 배치 처리 중 일부 URL 실패

**증상:**
```
📊 배치 처리 완료!
✅ 성공: 3개
❌ 실패: 1개
```

**일반적인 실패 원인:**

1. **존재하지 않는 게시물**
```bash
❌ 실패: 게시물이 삭제되었거나 존재하지 않습니다.
```
해결: URL 목록에서 해당 URL 제거

2. **비공개 계정**
```bash
❌ 실패: 비공개 계정입니다. 로그인이 필요합니다.
```
해결: 공개 계정의 게시물만 목록에 포함

3. **네트워크 오류**
```bash
❌ 실패: 네트워크 연결 오류
```
해결: `--delay` 옵션으로 대기시간 증가

**배치 처리 재시도 전략:**
```bash
# 1. 실패한 URL만 별도 파일로 생성
grep "FAILED_URL" debug.log > failed_urls.txt

# 2. 실패한 URL들만 재처리 (긴 대기시간)
PYTHONPATH=. ./.venv/bin/python -m src --batch-file failed_urls.txt --delay 10
```

### ⏱️ 배치 처리가 중단됨

**증상:**
```bash
🔄 처리 중... [2/4] https://www.instagram.com/p/ABC123/
^C  # 사용자가 Ctrl+C로 중단
```

**해결책:**

1. **진행상황 확인**
```bash
# outputs 디렉토리에서 처리된 파일 확인
ls -la outputs/
ls -la outputs/ | grep $(date +%Y%m%d)  # 오늘 처리된 파일만
```

2. **남은 URL들만 처리**
```bash
# 원본 URL 목록에서 처리된 URL 제거
# 수동으로 urls.txt 편집 또는:

# 처리된 URL 확인 후 새 목록 생성
tail -n +3 urls.txt > remaining_urls.txt  # 앞의 2개 제외하고 나머지
PYTHONPATH=. ./.venv/bin/python -m src --batch-file remaining_urls.txt
```

3. **통합 파일 재구성**
```bash
# 개별 파일들을 수동으로 통합
cat outputs/instagram_*_$(date +%Y%m%d)*.txt > combined_manual.txt
```

### 📦 통합 파일이 생성되지 않음

**증상:** 개별 파일은 저장되지만 통합 파일이 생성되지 않음

**원인:** `--combined-output` 옵션 누락

**해결책:**
```bash
# ❌ 개별 파일만 저장
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --save txt

# ✅ 개별 파일 + 통합 파일 저장
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --save txt --combined-output

# 기존 개별 파일들을 수동으로 통합
cat outputs/instagram_*_$(date +%Y%m%d)*.txt > outputs/manual_combined_$(date +%Y%m%d_%H%M%S).txt
```

### 🐌 배치 처리가 매우 느림

**증상:** 4개 URL 처리에 5분 이상 소요

**원인 및 해결:**

1. **Rate Limiting 대기시간이 너무 김**
```bash
# 현재 설정 확인 (기본 3초)
# 필요시 단축 (주의: Instagram 차단 위험)
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --delay 1

# 권장: 2초 이상 유지
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --delay 2
```

2. **네트워크 연결 최적화**
```bash
# 네트워크 속도 테스트
ping -c 4 instagram.com
curl -o /dev/null -s -w "%{time_total}\n" https://instagram.com

# WiFi/이더넷 재연결
```

3. **Instagram 서버 응답 지연**
```bash
# 시간대 변경 시도 (한국 시간 기준 새벽/오전 권장)
# 또는 잠시 후 재시도
```

### 🔍 배치 처리 디버깅

**상세 로그 생성:**
```bash
# 배치 처리 과정을 로그 파일로 저장
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata 2>&1 | tee batch_debug.log

# 로그 파일에서 에러만 확인
grep -i "error\|fail\|❌" batch_debug.log

# 성공률 확인
grep -c "✅ 성공" batch_debug.log
grep -c "❌ 실패" batch_debug.log
```

**테스트 배치 처리:**
```bash
# 작은 테스트 파일로 먼저 테스트
echo "https://www.instagram.com/p/DOiSOJwEvAT/" > test_urls.txt
PYTHONPATH=. ./.venv/bin/python -m src --batch-file test_urls.txt --metadata

# 성공하면 전체 목록으로 진행
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata --save txt --combined-output
```

## 성능 관련 문제

### ⏱️ 프로그램이 너무 느림

**증상:** 게시물 하나 처리에 30초 이상 소요

**원인:**
- 네트워크 연결 속도
- Instagram 서버 응답 지연
- Rate limiting

**해결책:**
1. **네트워크 최적화**
   ```bash
   # 네트워크 속도 테스트
   curl -o /dev/null -s -w "%{time_total}\n" https://instagram.com

   # WiFi 재연결 또는 유선 연결 시도
   ```

2. **대기시간 조정**
   ```bash
   # 연속 처리 시 간격 두기
   # 대화형 모드에서 각 URL 처리 후 2-3초 대기
   ```

### 🔄 "재시도 중" 메시지가 계속 나타남

**증상:**
```
[retrying; skip with ^C]
```

**해결책:**
1. **강제 중단 후 재시도**
   ```bash
   # Ctrl+C로 중단
   # 5-10분 대기 후 재실행
   ```

2. **다른 게시물로 테스트**
   ```bash
   # 다른 공개 게시물 URL로 테스트
   ```

## 일반적인 해결책

### 🔧 완전 초기화

모든 문제가 해결되지 않을 때:

```bash
# 1. 가상환경 삭제 및 재생성
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

# 2. 의존성 재설치
pip install --upgrade pip
pip install -r requirements.txt

# 3. 권한 설정
chmod +x .venv/bin/python

# 4. 테스트 실행
PYTHONPATH=. ./.venv/bin/python -m src --help
```

### 🧪 테스트 실행

프로그램이 정상적으로 설치되었는지 확인:

```bash
# 1. 단위 테스트 실행
PYTHONPATH=. ./.venv/bin/python -m pytest tests/ -v

# 2. 간단한 URL 테스트
PYTHONPATH=. ./.venv/bin/python -m src https://www.instagram.com/p/DOiSOJwEvAT/ --quiet

# 3. 대화형 모드 테스트
PYTHONPATH=. ./.venv/bin/python -m src
# quit으로 즉시 종료 가능
```

### 📞 추가 도움말

**환경 정보 수집:**
```bash
# Python 버전
python3 --version

# 시스템 정보
uname -a

# 가상환경 경로
which python
echo $PYTHONPATH

# 패키지 설치 상태
pip list | grep instaloader
```

**로그 파일 생성:**
```bash
# 상세한 오류 로그 저장
PYTHONPATH=. ./.venv/bin/python -m src [URL] 2>&1 | tee debug.log

# 디버그 정보 포함 실행
PYTHONPATH=. ./.venv/bin/python -v -m src [URL]
```

**일반적인 체크리스트:**
- [ ] 프로젝트 루트 디렉토리에서 실행
- [ ] PYTHONPATH=. 포함
- [ ] 가상환경 활성화 확인
- [ ] 올바른 Instagram URL 형식
- [ ] 인터넷 연결 상태 확인
- [ ] outputs 디렉토리 권한 확인

**배치 처리 추가 체크리스트:**
- [ ] URL 목록 파일 존재 및 권한 확인
- [ ] URL 목록 파일에 유효한 URL 포함
- [ ] `--combined-output` 옵션 포함 (통합 파일 필요시)
- [ ] `--delay` 값이 2초 이상
- [ ] 한 번에 처리하는 URL 수가 20개 이하

### 📈 배치 처리 성능 권장사항

**권장 사용량:**

**단일 URL 처리:**
- 연속 처리 시 요청 간 2-3초 간격 권장
- 시간당 50개 이하 게시물 처리 권장

**배치 처리:**
- `--delay` 옵션으로 2-3초 이상 설정 (기본값: 3초)
- 한 번에 10-20개 URL 이하 권장
- 50개 이상 처리 시 여러 배치로 분할
- Rate limiting 발생 시 10-15분 대기 후 재시도

**배치 처리 권장 패턴:**
```bash
# 작은 배치로 분할 처리
split -l 10 large_urls.txt batch_
# batch_aa, batch_ab, batch_ac... 파일들 생성

# 각 배치를 순차적으로 처리
for batch in batch_*; do
    echo "Processing $batch..."
    PYTHONPATH=. ./.venv/bin/python -m src --batch-file "$batch" --save txt --combined-output
    sleep 300  # 5분 대기
done
```

이 가이드로 해결되지 않는 문제가 있다면, 에러 메시지와 함께 이슈를 등록해 주세요.