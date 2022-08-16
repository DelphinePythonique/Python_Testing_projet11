import os

import pytest
from pytest_mock import mocker

from server import loadClubs, clubs_with_email, clubs


def test_should_load_clubs():
    if os.path.exists("clubs.json"):
        print('existe')
        clubs = loadClubs()
        club = clubs[0]

        assert isinstance(club, dict)
        assert ("name" in club) == True
        assert ("email" in club) == True
        assert ("points" in club) == True
        assert isinstance(int(club["points"]), int) == True

    if not os.path.exists("clubs.json"):
        with pytest.raises(FileNotFoundError):
            print('not existe')
            loadClubs()

def test_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_should_return_index_template(client):
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

def test_should_return_clubs_with_email_ok(clubs_fixture, mocker):
    mocker.patch('server.clubs', clubs_fixture)
    assert clubs_with_email("john@gudlft.ok") == [{
        "name":"Simply Lift",
        "email":"john@gudlft.ok",
        "points":"13"
    }]
    assert clubs_with_email("john@gudlft.ko") == []

def test_should_show_summary_ok(client, club_fixture, mocker):
    mocker.patch('server.clubs_with_email', return_value=club_fixture)
    email = "john@gudlft.ok"
    response = client.post("/showSummary", data={'email': email})
    data = response.data.decode("utf-8")
    assert response.status_code == 200

    mocker.patch('server.clubs_with_email', return_value=[])
    email = "john@gudlft.ok"
    response = client.post("/showSummary", data={'email': email})
    data = response.data.decode("utf-8")
    assert response.status_code == 302