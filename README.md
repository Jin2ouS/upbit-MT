# 업비트 크립토 감시/자동매매 (upbit-MT)

업비트 Open API를 사용하여 크립토 가격을 감시하고, 설정된 임계값에 도달 시 자동으로 매수/매도 주문을 실행하는 Python 스크립트입니다.

## 파일 구성

| 파일 | 역할 |
|------|------|
| `upbitMT.py` | 단일 실행 파일 |
| `utils.py` | Slack/Telegram 메시지 전송 |
| `.env` | 환경설정 (API 키, 알림 채널 등) |
| `upbitMT.list.xlsx` | 임계값 엑셀 (감시 대상/조건) |
| `requirements_upbitMT.txt` | Python 의존성 |

## 설치

```bash
pip install -r requirements_upbitMT.txt
```

## 설정 (.env)

`.env.example`을 복사하여 `.env`를 생성하고 값을 채웁니다.

```bash
cp .env.example .env
```

| 변수 | 설명 | 필수 |
|------|------|------|
| UPBIT_ACCESS_KEY | 업비트 Open API Access Key | O |
| UPBIT_SECRET_KEY | 업비트 Open API Secret Key | O |
| MONITOR_FILE | 임계값 엑셀 파일명 (예: upbitMT.list.xlsx) | - (기본값: upbitMT.list.xlsx) |
| ALARM_CHANNEL | slack 또는 telegram | O |
| SLACK_WEBHOOK_URL | Slack Webhook URL (ALARM_CHANNEL=slack 시) | O |
| TELEGRAM_BOT_TOKEN | 텔레그램 봇 토큰 (ALARM_CHANNEL=telegram 시) | O |
| TELEGRAM_CHAT_ID | 텔레그램 Chat ID (ALARM_CHANNEL=telegram 시) | O |

## 임계값 엑셀 형식 (upbitMT.list.xlsx)

autoMT.list.KIS.xlsx 형식을 따릅니다.

| 컬럼 | 설명 | 예시 |
|------|------|------|
| 종목명 | 종목 식별 (비트코인, BTC, KRW-BTC 등) | 비트코인 |
| 감시사유 | 감시 목적 설명 | 익절 |
| 매매구분 | 매수 / 매도 / 기준봉익절 | 매도 |
| 감시가격 | 목표가 (원화 또는 %) | 95000000 |
| 감시조건 | 이상 / 이하 | 이상 |
| 매매수량 | 수량 (숫자+코인 또는 %) | 0.001 또는 50% |
| 매매가격 | market(시장가) 또는 지정가액 | market |
| 유효기간 | 감시 종료일 | 2025-12-31 |
| 감시중 | O(감시) / X(미감시) | O |

- **종목명**: 비트코인, 이더리움, BTC, ETH, KRW-BTC 등 (마켓코드 자동 매핑)
- **감시가격**: 원화 숫자, 백분율(%), 기준봉익절(한콤마 숫자)
- **매매수량**: 매수 시 숫자 또는 숫자+코인 / 매도 시 숫자, %, 숫자+코인

## 실행

```bash
python upbitMT.py
```

## 컨테이너 배포 (Docker)

`.env` 대신 환경변수로 주입 가능합니다.

```bash
docker run -d \
  -e UPBIT_ACCESS_KEY=xxx \
  -e UPBIT_SECRET_KEY=xxx \
  -e MONITOR_FILE=upbitMT.list.xlsx \
  -e ALARM_CHANNEL=slack \
  -e SLACK_WEBHOOK_URL=https://hooks.slack.com/... \
  -v /path/to/upbitMT.list.xlsx:/app/upbitMT.list.xlsx \
  your-image python upbitMT.py
```

또는 `--env-file .env` 사용:

```bash
docker run -d --env-file .env -v $(pwd):/app your-image python upbitMT.py
```

## 주의사항

- API 키는 [업비트 마이페이지 > Open API 관리](https://upbit.com/mypage/open_api_management)에서 발급합니다.
- `.env` 파일은 Git에 커밋하지 마세요 (`.gitignore`에 포함됨).
- 실제 매매 전 테스트를 권장합니다.
