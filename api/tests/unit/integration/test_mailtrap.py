from unittest.mock import patch

import pytest

from config.app_config import AppConfig
from integrations.mailtrap import MailtrapClient


class TestMailtrap:
    @pytest.mark.asyncio
    @patch("builtins.print")
    @patch("integrations.mailtrap.requests")
    async def test_send_email(self, requests_mock, print_mock):
        requests_mock.post.return_value.status_code = 200
        mailtrap_client = MailtrapClient()
        await mailtrap_client.send_email("Email subject", "Email text")
        requests_mock.post.assert_called_with(
            url=f"{mailtrap_client.base_url}/send/{AppConfig.MAILTRAP_INBOX_NUMBER}",
            headers=mailtrap_client.headers,
            json={
                "from": {"email": "almirmulke4@gmail.com", "name": "Account creation exercise."},
                "to": [{"email": "almirmulke4@gmail.com", "name": "Almir"}],
                "subject": "Email subject",
                "text": "Email text",
            },
        )
        print_mock.assert_not_called()

    @pytest.mark.asyncio
    @patch("builtins.print")
    @patch("integrations.mailtrap.requests")
    async def test_send_email_failed_request(self, requests_mock, print_mock):
        requests_mock.post.return_value.status_code = 400
        mailtrap_client = MailtrapClient()
        await mailtrap_client.send_email("Email subject", "Email text")
        requests_mock.post.assert_called_with(
            url=f"{mailtrap_client.base_url}/send/{AppConfig.MAILTRAP_INBOX_NUMBER}",
            headers=mailtrap_client.headers,
            json={
                "from": {"email": "almirmulke4@gmail.com", "name": "Account creation exercise."},
                "to": [{"email": "almirmulke4@gmail.com", "name": "Almir"}],
                "subject": "Email subject",
                "text": "Email text",
            },
        )
        print_mock.assert_called_once_with("Activation code email was not sent successfully!")
