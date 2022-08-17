import os

from flask import get_flashed_messages
from jsonschema import validate
import pytest
from pytest_mock import mocker

from server import loadClubs, clubs_with_email


class TestServerClass:
    def test_should_index_ok(self, client):
        response = client.get("/")
        assert response.status_code == 200

        response = client.get("/")
        data = response.data.decode("utf-8")
        print(data)
        assert (
            data
            == """<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GUDLFT Registration</title>
</head>
<body>
    <h1>Welcome to the GUDLFT Registration Portal!</h1>
    
            
    Please enter your secretary email to continue:
    <form action="showSummary" method="post">
        <label for="email">Email:</label>
        <input type="email" name="email" id=""/>
        <button type="submit">Enter</button>
    </form>
  
</body>
</html>"""
        )

    def test_should_load_clubs(self, clubs_schema_fixture):
        assert os.path.exists("clubs.json")
        clubs = loadClubs()

        assert validate(instance=clubs, schema=clubs_schema_fixture) == None

    def test_should_return_clubs_with_email_ok(self, clubs_fixture, mocker):
        assert clubs_with_email(clubs_fixture, "john@gudlft.ok") == [
            {"name": "Simply Lift", "email": "john@gudlft.ok", "points": "13"}
        ]

    def test_should_return_clubs_with_email_ko(self, clubs_fixture, mocker):
        assert clubs_with_email(clubs_fixture, "john@gudlft.ko") == []

    def test_should_show_summary_with_email_ok(self, client, clubs_fixture, mocker):
        mocker.patch("server.loadClubs", return_value=clubs_fixture)
        email = "john@gudlft.ok"
        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == 200

        assert b"john@gudlft.ok" in response.data
        assert b"Competitions:" in response.data
        assert b"Spring Festival" in response.data
        assert b"Date: 2020-03-27 10:00:00" in response.data
        assert b"Number of Places:" in response.data
        assert (
            b'25\n            \n            <a href="/book/Spring%20Festival/Simply%20Lift">Book Places</a>'
            in response.data
        )

        assert b"Fall Classic" in response.data
        assert b"Date: 2020-10-22 13:30:00" in response.data
        assert b"Number of Places:" in response.data
        assert (
            b'13\n            \n            <a href="/book/Fall%20Classic/Simply%20Lift">Book Places</a>'
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
