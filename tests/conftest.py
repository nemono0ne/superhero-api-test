import pytest

from src.main import fetch_all_heroes

MALE = "Male"
FEMALE = "Female"
UNKNOWN = "-"


@pytest.fixture(scope="module")
def real_heroes() -> list[dict]:
    """
    Load data from Superhero API
    """
    return fetch_all_heroes()


@pytest.fixture(scope="module")
def heroes() -> list[dict]:
    """
    Mock data for unit tests.
    Covers cm/meters, job status, and different genders.
    """
    return [

        {"name": "MaleSmall", "appearance": {"gender": MALE, "height": ["", "100 cm"]}, "work": {"occupation": "Dev"}},
        {"name": "MaleTall", "appearance": {"gender": MALE, "height": ["", "200 cm"]}, "work": {"occupation": "Dev"}},
        {"name": "MaleNoJobSmall", "appearance": {"gender": MALE, "height": ["", "200 cm"]}, "work": {"occupation": UNKNOWN}},
        {"name": "MaleNoJobTall", "appearance": {"gender": MALE, "height": ["", "300 cm"]}, "work": {"occupation": UNKNOWN}},

        {"name": "FemaleSmall", "appearance": {"gender": FEMALE, "height": ["", "1.1 meters"]}, "work": {"occupation": "QA"}},
        {"name": "FemaleTall", "appearance": {"gender": FEMALE, "height": ["", "2.1 meters"]}, "work": {"occupation": "QA"}},
        {"name": "FemaleNoJobSmall", "appearance": {"gender": FEMALE, "height": ["", "5 cm"]}, "work": {"occupation": UNKNOWN}},
        {"name": "FemaleNoJobTall", "appearance": {"gender": FEMALE, "height": ["", "6 cm"]}, "work": {"occupation": UNKNOWN}},

        {"name": "UnknownSmall", "appearance": {"gender": UNKNOWN, "height": ["", "189 cm"]}, "work": {"occupation": "Spy"}},
        {"name": "UnknownNoJobSmall", "appearance": {"gender": UNKNOWN, "height": ["", "259 cm"]}, "work": {"occupation": UNKNOWN}},
        {"name": "UnknownTall", "appearance": {"gender": UNKNOWN, "height": ["", "190 cm"]}, "work": {"occupation": "Spy"}},
        {"name": "UnknownNoJobTall", "appearance": {"gender": UNKNOWN, "height": ["", "260 cm"]}, "work": {"occupation": UNKNOWN}},
    ]
