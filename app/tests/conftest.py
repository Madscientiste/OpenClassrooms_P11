import pytest

from app.data import clubs, competitions
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def data():
    return {"clubs": clubs, "competitions": competitions}
