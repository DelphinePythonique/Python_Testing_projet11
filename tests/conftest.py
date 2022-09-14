import enum
import os

import pytest


from server import app as myapp

DATABASE_DIRECTORY_FOR_TEST = "database/test/"
COMPETITIONS_TABLE = "competitions"
CLUBS_TABLE = "clubs"
BOOKINGS_TABLE = "bookings"
EMAIL_OK = "test1@project11.fr"
EMAIL_KO = "test1@project11.ko"
COMPETITION_OK = "competition test1"
COMPETITION2_OK = "competition test2"
COMPETITION_KO = "competition ko"
CLUB_OK = "test1"
CLUB_KO = "CLUB KO"
QUANTITY_PLACES_OK = 1
QUANTITY_PLACES_SUP_AVAILABLE = 8
QUANTITY_POINTS_SUP_AVAILABLE = 14


@pytest.fixture
def client():
    app = myapp
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def app():
    app = myapp
    return app


@pytest.fixture
def competitions_fixture():
    data = [
        {
            "name": "competition test1",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "6",
        },
        {
            "name": "competition test2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
    ]
    yield data


@pytest.fixture
def booking_fixture():
    data = [{"club": "test1", "competition": "competition test2", "booked_places": 2}]
    yield data


@pytest.fixture
def club_fixture():
    data = [{"name": "test1", "email": "test1@project11.fr", "points": "13"}]
    yield data


@pytest.fixture
def clubs_fixture():
    data = [
        {"name": "test1", "email": "test1@project11.fr", "points": "5"},
        {"name": "test2", "email": "test2@project11.fr", "points": "4"},
        {"name": "test3", "email": "test3@project11.fr", "points": "12"},
    ]

    yield data


@pytest.fixture
def competition_fixture():
    data = [
        {
            "name": "competition test2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "6",
        }
    ]
    yield data


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
    yield schema


@pytest.fixture
def clubs_schema_empty_fixture():
    schema = {
        "clubs_test": {"type": "array"},
    }
    yield schema


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
    yield schema


class TableNameMocker(enum.Enum):
    CLUBS = "clubs"
    COMPETITIONS = "competitions"
    BOOKINGS = "bookings"


class DataManagerMocker:
    class TableName(enum.Enum):
        CLUBS = "clubs"
        COMPETITIONS = "competitions"
        BOOKINGS = "bookings"

    @property
    def app(self):

        app = myapp
        return app


def refresh_datafiles():
    with open(f"{DATABASE_DIRECTORY_FOR_TEST}/clubs_save.json", "r") as myfile:
        data = myfile.read()

    with open(f"{DATABASE_DIRECTORY_FOR_TEST}/clubs.json", "w") as myfile:
        myfile.write(data)

    with open(f"{DATABASE_DIRECTORY_FOR_TEST}/competitions_save.json", "r") as myfile:
        data = myfile.read()

    with open(f"{DATABASE_DIRECTORY_FOR_TEST}/competitions.json", "w") as myfile:
        myfile.write(data)

    with open(f"{DATABASE_DIRECTORY_FOR_TEST}/bookings_save.json", "r") as myfile:
        data = myfile.read()

    with open(f"{DATABASE_DIRECTORY_FOR_TEST}/bookings.json", "w") as myfile:
        myfile.write(data)
