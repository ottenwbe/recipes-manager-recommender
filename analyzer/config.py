# Copyright (c) 2021 Beate Ottenwälder
# SPDX-License-Identifier: MIT

import yaml
import os.path

RECIPE_SERVER = "recipe-server"
DEFAULT_RECIPE_SERVER = "localhost:8080"


class RecipeStatsConfig:
    class __RecipeStatsConfig:
        def __init__(self):
            self.RECIPE_SERVER = DEFAULT_RECIPE_SERVER

        @staticmethod
        def _read_yaml(file_path):
            try:
                with open(file_path, "r") as f:
                    return yaml.safe_load(f)
            except FileNotFoundError:
                return {}

        def make_config(self):
            """Create a Config. Reads a config file and then"""
            if os.path.isfile("config.yml"):
                cfg_file = self._read_yaml("config.yml")
            else:
                cfg_file = self._read_yaml("/etc/recipes-recommendations/config.yml")
            if cfg_file.get(RECIPE_SERVER) is not None:
                self.RECIPE_SERVER = cfg_file.get(RECIPE_SERVER)

    instance = None

    # new singleton config class
    def __new__(cls):
        if not RecipeStatsConfig.instance:
            RecipeStatsConfig.instance = RecipeStatsConfig.__RecipeStatsConfig()
        return RecipeStatsConfig.instance
