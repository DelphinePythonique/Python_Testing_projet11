import pytest

from server import app as myapp

EMAIL_OK = "john@simplylift.co"
EMAIL_KO = "john@gudlft.ko"
COMPETITION_OK = "competition 1"
CLUB_OK = "CLUB A"
COMPETITION_KO = "competition ko"
CLUB_KO = "CLUB KO"

@pytest.fixture
def client():
    app = myapp
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def app():
    app = myapp
    app.debug = True
    app.config.from_object({"TESTING": True})
    return app


@pytest.fixture
def clubs_fixture():
    data = [
        {"name": "CLUB A", "email": "john@gudlft.ok", "points": "13"},
        {"name": "CLUB B", "email": "admin@irontemple.com", "points": "4"},
        {"name": "CLUB C", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    return data


@pytest.fixture
def competitions_fixture():
    data = [
        {
            "name": "competition 1",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "competition 2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
    ]
    return data


@pytest.fixture
def club_fixture():
    data = [{"name": "Simply Lift", "email": "john@gudlft.ok", "points": "13"}]
    return data


@pytest.fixture
def clubs_schema_fixture():
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "points": {"type": "string"},
            },
            "required": ["name", "email", "points"],
        },
    }
    return schema


@pytest.fixture
def competitions_schema_fixture():
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "date": {"type": "string"},
                "numberOfPlaces": {"type": "string"},
            },
            "required": ["name", "date", "numberOfPlaces"],
        },
    }
    return schema
