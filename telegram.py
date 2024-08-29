import requests
import os
from dotenv import load_dotenv

def send_telegram(message):
  load_dotenv()
  token = os.getenv("TELEGRAM_BOT_TOKEN")
  url = f"https://api.telegram.org/bot{token}"
  params = {"chat_id": "7491567269", "text": message}
  r = requests.get(url + "/sendMessage", params=params)
  if r.status_code != 200:
    raise ValueError(f"Request to Telegram API failed: {r.text}")
  else:
    print("Telegram sent to phone")