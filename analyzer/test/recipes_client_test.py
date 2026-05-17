import pytest
from analyzer import RECIPE_CONFIG
from analyzer.config import DEFAULT_RECIPE_SERVER, RecipeStatsConfig
from analyzer.recipes_client import Client
from requests_mock.mocker import Mocker


@pytest.fixture
def recipes_client():
    return Client()


def test_get_recipes(requests_mock: Mocker, recipes_client):
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes", json={"recipes": ["1"]}
    )
    result = recipes_client.get_recipes()
    assert {"recipes": ["1"]} == result


def test_get_recipes(requests_mock: Mocker, recipes_client):
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes",
        text="Not Found",
        status_code=404,
    )
    result = recipes_client.get_recipes()
    assert {"recipes": []} == result


def test_get_norecipes(requests_mock: Mocker, recipes_client):
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes", json={"recipes": []}
    )
    result = recipes_client.get_full_recipes()
    assert [] == result


def test_get_all_recipes(requests_mock: Mocker, recipes_client):
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes", json={"recipes": ["1"]}
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/1",
        json={"id": 1, "components": []},
    )
    result = recipes_client.get_full_recipes()
    assert [{"id": 1, "components": []}] == result


def test_get_wrong_recipes(requests_mock: Mocker, recipes_client):
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes", json={"recipes": ["1"]}
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/1",
        text="Not Found",
        status_code=404,
    )
    result = recipes_client.get_full_recipes()
    assert [] == result
