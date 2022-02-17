import pytest

from app.utilities import JsonLoader
from server import create_app

clubs = JsonLoader("clubs", testing=True)
competitions = JsonLoader("competitions", testing=True)


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "clubs": clubs, "competitions": competitions})
    with app.test_client() as client:
        yield client


@pytest.fixture
def data():
    return {"clubs": clubs, "competitions": competitions}
