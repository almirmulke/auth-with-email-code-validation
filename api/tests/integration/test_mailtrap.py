import pytest

from integrations.mailtrap import MailtrapClient


class TestMailtrapIntegration:
    pass

    @pytest.mark.asyncio
    async def test_mailtrap_call_happy_path(self):
        response = await MailtrapClient().send_email("Activation_code", "Email text")
        assert response.status_code == 200
