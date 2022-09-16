from flask import get_flashed_messages

from tests.conftest import (
    EMAIL_KO,
    EMAIL_OK,
    refresh_datafiles,
)


class TestIntegrationServerDisplayClubClass:
    def setup_method(self):
        refresh_datafiles()


    def test_login_with_email_ok(self, client):
        email = EMAIL_OK
        response = client.post("/login", data={"email": email})

        assert response.status_code == 302
        assert (
                b'You should be redirected automatically to target URL: <a href="/">/</a>'
                in response.data
        )

        flash_messages = get_flashed_messages()
        assert "congratulation you are connected" in flash_messages

    def test_login_with_email_ko(self, client, clubs_fixture, mocker):
        email = EMAIL_KO
        response = client.post("/login", data={"email": email})

        assert response.status_code == 302
        assert (
            b'You should be redirected automatically to target URL: <a href="/">/</a>'
            in response.data
        )

        flash_messages = get_flashed_messages()
        assert "email not existing" in flash_messages
