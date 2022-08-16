import pytest

from server import app as myapp


@pytest.fixture
def client():
    app = myapp
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture
def clubs_fixture():
    data = [
    {
        "name":"Simply Lift",
        "email":"john@gudlft.co",
        "points":"13"
    },
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },
    {   "name":"She Lifts 1",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }
]
    return data