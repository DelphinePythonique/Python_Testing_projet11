import pytest

from server import app as myapp

@pytest.fixture
def client():
    app = myapp
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='session')
def app():
    app = myapp
    app.config.from_object({
        "TESTING": True,

    })
    return app



@pytest.fixture
def clubs_fixture():
    data = [
        {"name": "Simply Lift", "email": "john@gudlft.ok", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts 1", "email": "kate@shelifts.co.uk", "points": "12"},
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
