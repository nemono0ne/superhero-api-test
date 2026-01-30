import requests
from typing import Optional

BASE_URL = "https://akabab.github.io/superhero-api/api/all.json"
TIMEOUT = 5
CM_UNIT = "cm"
METER_UNIT = "meter"
METERS_TO_CM = 100
UNKNOWN_VALUES = {"", "-"}


def fetch_all_heroes() -> list[dict]:
    """
    Load data from Superhero API.
    """

    response = requests.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def parse_height_cm(hero: dict) -> Optional[int]:
    """
    Returns hero height in centimeters.
    Handles:
      - cm
      - meters
      - '-' or empty --> returns None
    """
    heights = hero.get("appearance", {}).get("height", [])

    if len(heights) < 2:
        return None

    value = heights[1].strip().lower()
    if value in UNKNOWN_VALUES:
        return None

    try:
        num = float(value.split()[0])
        if num <= 0:
            return None
    except ValueError:
        return None

    if CM_UNIT in value:
        return int(num)
    if METER_UNIT in value:
        return int(num * METERS_TO_CM)
    return None


def has_job(hero: dict) -> bool:
    """
    Checks if the hero has a job(occupation).
    """
    occupation = hero.get("work", {}).get("occupation")

    if not occupation:
        return False

    return occupation.strip() not in UNKNOWN_VALUES


def  find_tallest_hero(heroes: list[dict], gender: str, with_job: bool) -> Optional[dict]:
    """
    Returns the tallest hero filtered by gender and job presence.
    """
    if not isinstance(gender, str):
        raise TypeError("gender must be str")
    if not isinstance(with_job, bool):
        raise TypeError("with_job must be bool")

    gender = gender.strip().lower()

    filtered = [
        hero
        for hero in heroes
        if hero.get("appearance", {}).get("gender", "").strip().lower() == gender
        and has_job(hero) == with_job
        and parse_height_cm(hero) is not None
    ]

    if not filtered:
        return None

    return max(filtered, key=parse_height_cm)


def get_tallest_hero(gender: str, with_job: bool) -> Optional[dict]:
    """
    Returns the tallest Hero that meets the criteria from the API.(Main)
    """
    heroes = fetch_all_heroes()
    return find_tallest_hero(heroes, gender, with_job)
