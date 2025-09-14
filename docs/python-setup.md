# Python 개발환경 설정 가이드 (MacBook + VS Code)

MacBook과 VS Code를 사용한 Python 개발환경 설정을 단계별로 안내합니다.

## 1. 사전 준비

### Homebrew 설치
macOS용 패키지 매니저인 Homebrew를 설치합니다.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## 2. Python 설치

### 방법 1: pyenv 사용 (권장)
여러 Python 버전을 관리할 수 있는 pyenv를 사용합니다.

```bash
# pyenv 설치
brew install pyenv

# .zshrc에 설정 추가
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 터미널 재시작 또는 설정 적용
source ~/.zshrc

# Python 3.11 설치
pyenv install 3.11.0
pyenv global 3.11.0

# 설치 확인
python --version
```

### 방법 2: Homebrew로 직접 설치
```bash
brew install python@3.11
```

## 3. VS Code 설정

### 필수 확장 프로그램 설치
1. **Python** (Microsoft 공식)
2. **Pylance** (언어 서버)
3. **Python Docstring Generator**
4. **Python Indent**
5. **Black Formatter** (코드 포매팅)

### VS Code 설정 파일 구성
프로젝트 루트에 `.vscode/settings.json` 파일을 생성합니다.

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

## 4. 프로젝트 설정

### 가상환경 생성 및 활성화
```bash
# 프로젝트 디렉토리로 이동
cd your_project_directory

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate

# (가상환경 비활성화는 deactivate 명령어)
```

### VS Code에서 Python 인터프리터 설정
1. `Cmd + Shift + P`로 명령 팔레트 열기
2. "Python: Select Interpreter" 검색 후 선택
3. `./venv/bin/python` 선택

### 개발 도구 설치
```bash
# 기본 개발 도구들
pip install --upgrade pip
pip install black flake8 mypy pytest

# Jupyter 노트북 (필요시)
pip install jupyter

# 웹 개발용 (필요시)
pip install flask django fastapi

# 데이터 분석용 (필요시)
pip install pandas numpy matplotlib seaborn
```

## 5. 프로젝트 구조

권장하는 Python 프로젝트 구조입니다.

```
your_project/
├── venv/                 # 가상환경 (git에 포함하지 않음)
├── src/                  # 소스 코드
│   ├── __init__.py
│   └── main.py
├── tests/                # 테스트 코드
│   ├── __init__.py
│   └── test_main.py
├── docs/                 # 문서
├── .vscode/              # VS Code 설정
│   └── settings.json
├── .gitignore
├── requirements.txt      # 의존성 목록
├── requirements-dev.txt  # 개발용 의존성
└── README.md
```

## 6. 의존성 관리

### requirements.txt 생성 및 관리
```bash
# 현재 설치된 패키지 목록을 파일로 저장
pip freeze > requirements.txt

# 다른 환경에서 같은 패키지들 설치
pip install -r requirements.txt
```

### 개발용 의존성 분리
```bash
# 개발용 도구들을 별도 파일로 관리
echo "black==23.3.0" > requirements-dev.txt
echo "flake8==6.0.0" >> requirements-dev.txt
echo "mypy==1.3.0" >> requirements-dev.txt
echo "pytest==7.3.1" >> requirements-dev.txt

# 개발용 패키지 설치
pip install -r requirements-dev.txt
```

## 7. .gitignore 설정

Python 프로젝트용 `.gitignore` 파일:

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Environments
.env
.venv
```

## 8. 코드 품질 관리

### 코드 포매팅 (Black)
```bash
# 현재 디렉토리의 모든 Python 파일 포매팅
black .

# 특정 파일 포매팅
black src/main.py
```

### 린팅 (Flake8)
```bash
# 코드 스타일 검사
flake8 src/

# 설정 파일 (.flake8)
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

### 타입 검사 (mypy)
```bash
# 타입 힌트 검사
mypy src/
```

### 테스트 실행 (pytest)
```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=src tests/
```

## 9. 추가 팁

### 터미널에서 Python 경로 확인
```bash
which python
which pip
python -c "import sys; print(sys.executable)"
```

### VS Code 단축키
- `Cmd + Shift + P`: 명령 팔레트
- `F5`: 디버깅 시작
- `Shift + Enter`: 선택된 코드를 Python 터미널에서 실행

### 가상환경 자동 활성화
프로젝트 폴더 진입 시 자동으로 가상환경을 활성화하려면 `direnv`를 사용할 수 있습니다.

```bash
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
```

## 트러블슈팅

### Python 버전 충돌 문제
```bash
# 현재 Python 경로 확인
which python

# pyenv로 관리되는 버전 목록
pyenv versions

# 특정 버전으로 전환
pyenv local 3.11.0
```

### VS Code에서 모듈을 찾을 수 없는 경우
1. Python 인터프리터가 올바른 가상환경을 가리키는지 확인
2. `PYTHONPATH` 환경변수 설정
3. VS Code 재시작

이제 MacBook과 VS Code에서 Python 개발을 시작할 수 있습니다!