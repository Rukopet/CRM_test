import requests


class telegram_notification:
    TELEGRAM_URL = "https://api.telegram.org/bot"
    TUTORIAL_BOT_TOKEN = "1860214086:AAFw1RN499MRuTqVGUs9yY6mNOgLiZONetM"

    def send_message(self, message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{self.TELEGRAM_URL}{self.TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )
