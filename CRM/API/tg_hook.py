import requests
from django.http import JsonResponse

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = "1860214086:AAFw1RN499MRuTqVGUs9yY6mNOgLiZONetM"


class telegram_notification:
    TELEGRAM_URL = "https://api.telegram.org/bot"
    TUTORIAL_BOT_TOKEN = "1860214086:AAFw1RN499MRuTqVGUs9yY6mNOgLiZONetM"

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )
        return JsonResponse({"ok": "POST request processed"})
