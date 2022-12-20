import requests

from config.app_config import AppConfig
from utils.singleton import Singleton


class MailtrapClient(Singleton):
    def __init__(self):
        self.base_url = "https://sandbox.api.mailtrap.io/api"
        self.headers = {"Content-Type": "application/json", "Api-Token": AppConfig.MAILTRAP_API_KEY}

    async def send_email(self, subject, text):
        response = requests.post(
            url=f"{self.base_url}/send/{AppConfig.MAILTRAP_INBOX_NUMBER}",
            headers=self.headers,
            json={
                "from": {"email": "almirmulke4@gmail.com", "name": "Account creation exercise."},
                "to": [{"email": "almirmulke4@gmail.com", "name": "Almir"}],
                "subject": subject,
                "text": text,
            },
        )
        if 400 <= response.status_code <= 499:
            # log that email was not sent to user
            print("Activation code email was not sent successfully!")

        return response
