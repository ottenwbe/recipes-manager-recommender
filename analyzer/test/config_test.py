import os
import pytest

from analyzer import config
from analyzer.config import DEFAULT_RECIPE_SERVER, RecipeStatsConfig


def test_default_config():
    cfg1 = RecipeStatsConfig()
    cfg1.make_config()
    assert cfg1.RECIPE_SERVER == DEFAULT_RECIPE_SERVER


def test_singleton_config():
    cfg1 = RecipeStatsConfig()
    cfg1.RECIPE_SERVER = "test"
    cfg2 = RecipeStatsConfig()
    assert cfg2.RECIPE_SERVER == "test"


def test_read_yml_config():
    try:
        with open("config.yml", "w") as writer:
            writer.write(config.RECIPE_SERVER + ": ahost:123")
        cfg1 = RecipeStatsConfig()
        cfg1.make_config()
        assert cfg1.RECIPE_SERVER == "ahost:123"
    finally:
        os.remove("config.yml")
