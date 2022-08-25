import enum
import os

import pytest

os.environ["FLASK_ENV"] = "testing"

from server import app as myapp

DATABASE_DIRECTORY_FOR_TEST = "database/test/"
CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST = "clubs_test"
CLUB_TABLE_READONLY = "clubs"
EMAIL_OK = "test1@project11.fr"
EMAIL_KO = "test1@project11.ko"
COMPETITION_OK = "competition test1"
COMPETITION_KO = "competition ko"
CLUB_OK = "test1"
CLUB_KO = "CLUB KO"
QUANTITY_PLACES_OK = 1
QUANTITY_PLACES_SUP_AVAILABLE = 8
QUANTITY_POINTS_SUP_AVAILABLE = 14


@pytest.fixture
def client():
    app = myapp
    app.config.from_pyfile("./settings/test.cfg")
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def app():
    app = myapp
    app.config.from_pyfile("./settings/test.cfg")
    yield app


@pytest.fixture
def clubs_fixture():
    data = [
        {"name": "CLUB A", "email": "john@gudlft.ok", "points": "13"},
        {"name": "CLUB B", "email": "admin@irontemple.com", "points": "4"},
        {"name": "CLUB C", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    yield data


@pytest.fixture
def clubs_ready_to_dump_fixture():
    data = {
        CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST: [
            {"name": "CLUB A", "email": "john@gudlft.ok", "points": "13"},
            {"name": "CLUB B", "email": "admin@irontemple.com", "points": "4"},
            {"name": "CLUB C", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
    }
    yield data


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
    yield data


@pytest.fixture
def club_fixture():
    data = [{"name": "Simply Lift", "email": "john@gudlft.ok", "points": "13"}]
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
    CLUBS = "clubs_test"
    COMPETITIONS = "competitions_test"
    BOOKINGS = "bookings_test"


class DataManagerMocker:
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