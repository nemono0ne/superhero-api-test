from typing import Optional

import pytest
from src.main import get_tallest_hero, parse_height_cm, has_job, find_tallest_hero
from tests.conftest import MALE, FEMALE, UNKNOWN


@pytest.mark.integration
class TestIntegrationAPI:
    """
    Integration tests API.
    """

    def test_api_availability(self, real_heroes: list[dict]) -> None:
        """
        Checks if API is up and returns expected hero structure.
        """
        assert isinstance(real_heroes, list)
        assert len(real_heroes) > 0

        sample = real_heroes[0]
        assert all(key in sample for key in ["id", "name", "appearance", "work"])
        assert "gender" in sample["appearance"]
        assert "height" in sample["appearance"]

    @pytest.mark.parametrize("gender, has_job_flag", [
        (MALE, True),
        (FEMALE, True),
        (MALE, False),
        (FEMALE, False),
        (UNKNOWN, False),
    ])
    def test_get_tallest_hero_functional(self, gender: str, has_job_flag: bool) -> None:
        """
        Checks if the main function works correctly with live data.
        """
        result = get_tallest_hero(gender, has_job_flag)
        if result:
            assert result["appearance"]["gender"].lower() == gender.lower()
            assert has_job(result) == has_job_flag

    def test_case_insensitivity(self) -> None:
        """
        Checks the gender search parameter is case-insensitivity when calling the API.
        """
        res_low = get_tallest_hero("male", True)
        res_up = get_tallest_hero("MALE", True)
        assert res_low["id"] == res_up["id"]

    @pytest.mark.parametrize("gender, has_work", [
        (123, False),
        ("Male", "true")
    ])
    def test_input_validation(self, gender: str, has_work: bool) -> None:
        """
        Checks passing incorrect data types triggers a TypeError exception.
        """
        with pytest.raises(TypeError):
            get_tallest_hero(gender, has_work)


class TestHeightParsing:
    """
    Unit tests for helper functions that parse and validate hero data.
    """

    @pytest.mark.parametrize("height_data, expected", [
        (["6'8", "203 cm"], 203),
        (["6'8", "203 CM"], 203),
        (["6'0", "183 Cm"], 183),
        (["-", "183.1 Cm"], 183),
        (["50'", "15.2 meters"], 1520),
        (["0", "1.1 MeterS"], 110),
        (["-", "0 cm"], None),
        (["-", "-"], None),
        ([], None),
        (["-", "one meter"], None),
        (["-", "100"], None),
        (["-", "-50 cm"], None)
    ])
    def test_height_conversion(self, height_data: list[str], expected: Optional[int]) -> None:
        """
        Check if height strings are correctly converted to cm.
        """
        hero = {"appearance": {"height": height_data}}
        assert parse_height_cm(hero) == expected

    @pytest.mark.parametrize("occupation, expected", [
        ("Businessman", True),
        ("", False),
        ("-", False),
        (None, False),
    ])
    def test_has_job(self, occupation: Optional[str], expected: bool) -> None:
        """
        Checks if the hero has a job(occupation).
        """
        hero = {"work": {"occupation": occupation}}
        assert has_job(hero) == expected


class TestHeroFiltering:
    """
    Unit tests for the core filtering and search logic using local mock data.
    """

    @pytest.mark.parametrize(
        "gender, has_work, expected_name",
        [
            (MALE, True, "MaleTall"),
            (MALE, False, "MaleNoJobTall"),
            (FEMALE, True, "FemaleTall"),
            (FEMALE, False, "FemaleNoJobTall"),
            (UNKNOWN, True, "UnknownTall"),
            (UNKNOWN, False, "UnknownNoJobTall"),
        ],
    )
    def test_find_tallest_by_gender_and_job(self, heroes: list[dict], gender: str, has_work: bool, expected_name: str) -> None:
        """
        Checks the tallest hero is found among local candidates.
        """
        result = find_tallest_hero(heroes, gender, has_work)

        assert result is not None
        assert result["name"] == expected_name

    def test_find_tallest_hero_no_match(self) -> None:
        """
        Checks the function returns None when no hero matches the specified criteria.
        """
        heroes = [{"appearance": {"gender": FEMALE, "height": ["", "150 cm"]}, "work": {"occupation": "-"}}]
        assert find_tallest_hero(heroes, MALE, True) is None
