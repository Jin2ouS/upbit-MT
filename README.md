# upbit-MT

Monitor and Trade Crypto in Upbit

Automated cryptocurrency monitoring and trading system for Upbit exchange using Open API.

## Features

- Real-time price monitoring with Excel-based threshold configuration
- Automatic buy/sell order execution
- Multiple trade types: market orders, limit orders, percentage-based trading
- Telegram/Slack notifications
- Holdings display with valuation and profit/loss tracking

## File Structure

| File | Description |
|------|-------------|
| `upbitMT.py` | Main executable script |
| `utils.py` | Slack/Telegram messaging utilities |
| `.env` | Environment configuration (API keys, notification channels) |
| `upbitMT.list.xlsx` | Excel threshold configuration (monitoring targets/conditions) |
| `requirements_upbitMT.txt` | Python dependencies |

## Installation

```bash
pip install -r requirements_upbitMT.txt
```

## Configuration (.env)

Copy `.env.example` to `.env` and fill in your values.

```bash
cp .env.example .env
```

| Variable | Description | Required |
|----------|-------------|----------|
| UPBIT_ACCESS_KEY | Upbit Open API Access Key | Yes |
| UPBIT_SECRET_KEY | Upbit Open API Secret Key | Yes |
| MONITOR_FILE | Threshold Excel filename (e.g., upbitMT.list.xlsx) | No (default: upbitMT.list.xlsx) |
| ALARM_CHANNEL | slack or telegram | Yes |
| SLACK_WEBHOOK_URL | Slack Webhook URL (if ALARM_CHANNEL=slack) | Yes |
| TELEGRAM_BOT_TOKEN | Telegram Bot Token (if ALARM_CHANNEL=telegram) | Yes |
| TELEGRAM_CHAT_ID | Telegram Chat ID (if ALARM_CHANNEL=telegram) | Yes |

## Excel Threshold Format (upbitMT.list.xlsx)

| Column | Description | Example |
|--------|-------------|---------|
| 종목명 | Asset identifier (Bitcoin, BTC, KRW-BTC, etc.) | Bitcoin |
| 감시사유 | Monitoring reason | Take profit |
| 매매구분 | Trade type (매수/매도/기준봉익절) | 매도 |
| 감시가격 | Target price (KRW or %) | 95000000 |
| 감시조건 | Condition (이상/이하) | 이상 |
| 매매수량 | Quantity (number) | 0.001 or 50 |
| 매매단위 | Unit (개/KRW/%) | % |
| 매매가격 | market or limit price | market |
| 유효기간 | Expiry date | 2025-12-31 |
| 감시중 | O (active) / X (inactive) | O |

## Usage

```bash
python upbitMT.py
```

## Docker Deployment

Environment variables can be injected instead of using `.env`:

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

Or use `--env-file`:

```bash
docker run -d --env-file .env -v $(pwd):/app your-image python upbitMT.py
```

## Important Notes

- Get API keys from [Upbit MyPage > Open API Management](https://upbit.com/mypage/open_api_management)
- Never commit `.env` file (included in `.gitignore`)
- Test thoroughly before live trading

## License

Apache-2.0
