import requests
import os
from dotenv import load_dotenv

def send_telegram_message(message):
  load_dotenv()
  token = os.getenv("TELEGRAM_BOT_TOKEN")
  url = f"https://api.telegram.org/bot{token}"
  params = {"chat_id": "7491567269", "text": message}
  requests.get(url + "/sendMessage", params=params)

send_telegram_message()