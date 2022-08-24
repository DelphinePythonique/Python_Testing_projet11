import os

import pytest

os.environ['FLASK_ENV'] = "testing"

from server import app as myapp

@pytest.fixture
def client():
    app = myapp
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client