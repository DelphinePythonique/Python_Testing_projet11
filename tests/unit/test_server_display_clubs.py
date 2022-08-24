from flask import get_flashed_messages

from tests.conftest import EMAIL_KO, EMAIL_OK


class TestServerDisplayClubClass:
    def test_should_index_ok(self, client):
        response = client.get("/")
        assert response.status_code == 200

        response = client.get("/")

        assert b"Welcome to the GUDLFT Registration Portal!" in response.data
        assert b'<label for="email">Email:</label>' in response.data
        assert b'<input type="email" name="email" id=""/>' in response.data
        assert b'<button type="submit">Enter</button>' in response.data

    def test_should_show_summary_with_email_ok(self, client, clubs_fixture, competitions_fixture, mocker):
        email = EMAIL_OK
        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == 200
        print(response.data)
        assert b"test1@project11.fr" in response.data
        assert b"Competitions:" in response.data
        assert b"competition test1" in response.data
        assert b"Date: 2020-03-27 10:00:00" in response.data
        assert b"Number of Places:" in response.data
        assert (
                b'25\n            \n            <a href="/book/competition%20test1/test1">Book Places</a>'
                in response.data
        )

        assert b"competition test1" in response.data
        assert b"Date: 2020-10-22 13:30:00" in response.data
        assert b"Number of Places:" in response.data
        assert (
                b'13\n            \n            <a href="/book/competition%20test2/test1">Book Places</a>'
                in response.data
        )

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
