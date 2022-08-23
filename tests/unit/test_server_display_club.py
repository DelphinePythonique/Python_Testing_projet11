import os

from flask import get_flashed_messages
from jsonschema import validate


from server import loadClubs, clubs_with_email


class TestServerDisplayClubClass:
    def test_should_index_ok(self, client):
        response = client.get("/")
        assert response.status_code == 200

        response = client.get("/")

        assert b"Welcome to the GUDLFT Registration Portal!" in response.data
        assert b'<label for="email">Email:</label>' in response.data
        assert b'<input type="email" name="email" id=""/>' in response.data
        assert b'<button type="submit">Enter</button>' in response.data

    def test_should_load_clubs(self, clubs_schema_fixture):
        assert os.path.exists("db/test/clubs.json")
        clubs = loadClubs()

        assert validate(instance=clubs, schema=clubs_schema_fixture) is None

    def test_should_return_clubs_with_email_ok(self, clubs_fixture):
        assert clubs_with_email(clubs_fixture, "john@gudlft.ok") == [
            {"name": "CLUB A", "email": "john@gudlft.ok", "points": "13"}
        ]

    def test_should_return_clubs_with_email_ko(self, clubs_fixture, mocker):
        assert clubs_with_email(clubs_fixture, "john@gudlft.ko") == []

    def test_should_show_summary_with_email_ok(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch("server.loadClubs", return_value=clubs_fixture)
        mocker.patch("server.loadCompetitions", return_value=competitions_fixture)
        email = "john@gudlft.ok"
        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == 200
        print (response.data)
        assert b"john@gudlft.ok" in response.data
        assert b"Competitions:" in response.data
        assert b"competition 1" in response.data
        assert b"Date: 2020-03-27 10:00:00" in response.data
        assert b"Number of Places:" in response.data
        assert (
            b'25\n            \n            <a href="/book/competition%201/CLUB%20A">Book Places</a>'
            in response.data
        )

        assert b"competition 2" in response.data
        assert b"Date: 2020-10-22 13:30:00" in response.data
        assert b"Number of Places:" in response.data
        assert (
            b'13\n            \n            <a href="/book/competition%202/CLUB%20A">Book Places</a>'
            in response.data
        )

    def test_should_show_summary_with_email_ko(self, client, clubs_fixture, mocker):

        mocker.patch("server.loadClubs", return_value=[])
        email = "john@gudlft.ok"
        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == 302
        print(response.data)
        assert (
            b'You should be redirected automatically to target URL: <a href="/">/</a>'
            in response.data
        )

        flash_messages = get_flashed_messages()
        assert "email not existing" in flash_messages
