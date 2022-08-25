from flask import get_flashed_messages

from tests.conftest import EMAIL_KO, EMAIL_OK, DATABASE_DIRECTORY_FOR_TEST, refresh_datafiles


class TestIntegrationServerDisplayClubClass:
    def setup_method(self):
        refresh_datafiles()

    def test_should_show_summary_with_email_ok(self, client):
        email = EMAIL_OK
        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == 200

        assert b"test1@project11.fr" in response.data
        assert b"Competitions:" in response.data
        assert b"competition test1" in response.data
        assert b"Date: 2020-03-27 10:00:00" in response.data


        assert b"competition test1" in response.data
        assert b"Date: 2020-10-22 13:30:00" in response.data



    def test_should_show_summary_with_email_ko(self, client, clubs_fixture, mocker):
        email = EMAIL_KO
        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == 302
        print(response.data)
        assert (
                b'You should be redirected automatically to target URL: <a href="/">/</a>'
                in response.data
        )

        flash_messages = get_flashed_messages()
        assert "email not existing" in flash_messages

