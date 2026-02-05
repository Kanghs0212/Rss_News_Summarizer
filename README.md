# Automated Tech & Security News Briefing

매일 아침 AI, 사이버 보안, 빅테크 관련 주요 뉴스를 RSS로 수집하고, Google Gemini API를 활용하여 요약한 뒤, HTML 형식의 뉴스레터로 이메일을 발송하는 자동화 프로젝트입니다.

## 주요 기능

* **RSS 데이터 수집**: The Hacker News, Google Research, NVIDIA Blog 등 약 20여 개의 주요 기술 및 보안 관련 RSS 피드에서 최신 기사를 수집합니다.
* **AI 기반 요약**: Google Gemini 3.0 Flash 모델을 사용하여 각 기사를 한글로 2줄 내외로 핵심만 요약합니다.
* **HTML 이메일 생성**: 가독성을 위해 CSS 스타일링이 적용된 HTML 리포트를 자동으로 생성합니다.
* **자동 발송**: SMTP를 통해 지정된 Gmail 계정으로 요약 리포트를 발송합니다.
* **GitHub Actions 자동화**: 별도의 서버 없이 GitHub Actions를 통해 매일 오전 8시(KST)에 자동으로 실행됩니다.

## 기술 스택

* **Language**: Python 3.10
* **AI Model**: Google Gemini 3.0 Flash
* **Libraries**:
* `feedparser`: RSS 피드 파싱
* `google-generativeai`: Gemini API 연동
* `python-dotenv`: 환경 변수 관리


* **Infrastructure**: GitHub Actions (Cron Scheduler)

## 프로젝트 구조

```
.
├── .github/workflows/
│   └── daily_news.yml   # GitHub Actions 스케줄링 설정
├── email_sender.py      # HTML 메일 발송 모듈
├── main.py              # 전체 프로세스 실행 진입점
├── rss_collector.py     # RSS 수집 및 데이터 전처리 모듈
├── summarizer.py        # Gemini AI 요약 및 HTML 생성 모듈
├── requirements.txt     # 의존성 라이브러리 목록
└── .env                 # 로컬 환경 변수 (GitHub에 업로드 금지)

```

## 설치 및 실행 (로컬 환경)

### 1. 저장소 복제 (Clone)

```bash
git clone https://github.com/사용자명/레포지토리명.git
cd 레포지토리명

```

### 2. 가상 환경 생성 및 의존성 설치

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

```

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 아래 정보를 입력합니다.

* **GEMINI_API_KEY**: Google AI Studio에서 발급받은 API 키
* **GMAIL_USER**: 발송할 Gmail 주소
* **GMAIL_APP_PASSWORD**: Google 계정 설정에서 생성한 16자리 앱 비밀번호

```text
GEMINI_API_KEY=your_api_key_here
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password

```

### 4. 실행

```bash
python main.py

```

## GitHub Actions 설정 (자동화)

이 프로젝트를 매일 자동으로 실행하려면 GitHub Repository 설정이 필요합니다.

1. GitHub 저장소의 **Settings** > **Secrets and variables** > **Actions**로 이동합니다.
2. **New repository secret**을 클릭하여 아래 변수들을 등록합니다. (값은 `.env` 파일과 동일)
* `GEMINI_API_KEY`
* `GMAIL_USER`
* `GMAIL_APP_PASSWORD`


3. 설정이 완료되면 `.github/workflows/daily_news.yml`에 정의된 일정(매일 KST 08:00)에 따라 자동으로 실행됩니다.

## 참고 사항

* **스케줄 변경**: `.github/workflows/daily_news.yml` 파일 내 `cron` 값을 수정하여 실행 시간을 변경할 수 있습니다. (기본값: `'0 23 * * *'` - UTC 기준)
* **RSS 목록 추가**: `rss_collector.py` 파일의 `RSS_URLS` 리스트에 원하는 RSS 주소를 추가하면 즉시 반영됩니다.