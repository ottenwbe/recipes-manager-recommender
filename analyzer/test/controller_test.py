import os
import tempfile

import pytest

from requests_mock.mocker import Mocker

from analyzer import RECIPE_CONFIG, app, recipes_client


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_recipe_cache():
    recipes_client.DEFAULT_CLIENT.clear_cache()
    yield
    recipes_client.DEFAULT_CLIENT.clear_cache()


def test_root(client):
    """Test /"""

    result = client.get("/")
    assert b"Recipes Analyzer" in result.data


def test_similarity_simple(requests_mock: Mocker, client):
    """Test recommendation"""
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes", json={"recipes": ["1", "2"]}
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/1",
        json={"id": "1", "components": [{"name": "a"}]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/2",
        json={"id": "2", "components": [{"name": "a"}, {"name": "b"}]},
    )

    result = client.get("/api/v1/recommendation/1/components")

    assert {"recipes": ["2"]} == result.json


def test_similarity_num(requests_mock: Mocker, client):
    """Test recommendation"""
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes",
        json={"recipes": ["1", "2", "3", "4", "5"]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/1",
        json={"id": "1", "components": [{"name": "a"}, {"name": "b"}]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/2",
        json={"id": "2", "components": [{"name": "a"}]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/3",
        json={"id": "3", "components": [{"name": "a"}, {"name": "d"}]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/4",
        json={"id": "4", "components": [{"name": "e"}]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/5",
        json={"id": "5", "components": [{"name": "a"}, {"name": "b"}, {"name": "c"}]},
    )

    result = client.get("/api/v1/recommendation/1/components?num=2")

    assert {"recipes": ["5", "2"]} == result.json


def test_similarity_empty_component(requests_mock: Mocker, client):
    """Test recommendation"""
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes", json={"recipes": ["1", "2"]}
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/1",
        json={"id": "1", "components": [{"name": "a"}]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/2",
        json={"id": "2", "components": []},
    )

    result = client.get("/api/v1/recommendation/1/components")

    assert {"recipes": ["2"]} == result.json


def test_similarity_reuses_recipe_catalog_between_requests(
    requests_mock: Mocker, client
):
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes", json={"recipes": ["1", "2"]}
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/1",
        json={"id": "1", "components": [{"name": "a"}]},
    )
    requests_mock.get(
        RECIPE_CONFIG.RECIPE_SERVER + "/api/v1/recipes/r/2",
        json={"id": "2", "components": [{"name": "a"}, {"name": "b"}]},
    )

    first_result = client.get("/api/v1/recommendation/1/components")
    second_result = client.get("/api/v1/recommendation/1/components")

    assert {"recipes": ["2"]} == first_result.json
    assert {"recipes": ["2"]} == second_result.json
    assert requests_mock.call_count == 3
