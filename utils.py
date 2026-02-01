"""
Filename    : utils.py [/upbit-MT/]
Author      : [Jin2ouS]
Date        : 2025-02-01
Description : 메시지 전송 (Slack/Telegram), get_runtime_info 등
              .env 파일 기반 설정 로드
"""

import os
import re
import json
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

ALARM_CHANNEL = os.getenv("ALARM_CHANNEL", "slack").lower()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "").strip()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

if not ALARM_CHANNEL:
    raise ValueError("ALARM_CHANNEL(slack/telegram)이 .env에 없습니다.")

if ALARM_CHANNEL == "slack" and not SLACK_WEBHOOK_URL:
    raise ValueError("Slack 사용 시 SLACK_WEBHOOK_URL이 .env에 없습니다.")
elif ALARM_CHANNEL == "telegram" and (not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID):
    raise ValueError("Telegram 사용 시 TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID가 .env에 없습니다.")


def get_runtime_info():
    try:
        import socket
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        pid = os.getpid()
        in_docker = os.path.exists("/.dockerenv")
        return f"{hostname}, {ip_address}, PID: {pid}, Docker: {'Yes' if in_docker else 'No'}"
    except Exception:
        return "(시스템 정보 확인 실패)"


def send_slack_message(text, slack_webhook_url):
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(slack_webhook_url, headers=headers, data=json.dumps(payload), timeout=10)
    except Exception as e:
        print(f"[슬랙 전송 실패] {e}")


def send_telegram_message(text, bot_token, chat_id):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code != 200:
            error_data = response.json() if response.text else {}
            print(f"[텔레그램 전송 실패] HTTP {response.status_code}: {error_data}")
    except Exception as e:
        print(f"[텔레그램 전송 실패] {e}")


def convert_slack_to_telegram_format(text):
    """Slack 형식 링크(<url|text>)를 텔레그램 HTML 형식(<a href="url">text</a>)으로 변환"""
    pattern = r'<([^|>]+)\|([^>]+)>'
    def replace_link(match):
        url = match.group(1)
        link_text = match.group(2)
        return f'<a href="{url}">{link_text}</a>'
    return re.sub(pattern, replace_link, text)


def send_message(text):
    if ALARM_CHANNEL == "telegram":
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            telegram_text = convert_slack_to_telegram_format(text)
            send_telegram_message(telegram_text, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        else:
            print("[텔레그램 설정 누락] TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID가 없습니다.")
    else:
        if SLACK_WEBHOOK_URL:
            send_slack_message(text, SLACK_WEBHOOK_URL)
        else:
            print("[슬랙 설정 누락] SLACK_WEBHOOK_URL이 없습니다.")
