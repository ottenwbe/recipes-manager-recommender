# MIT License
#
# Copyright (c) 2021 Beate Ottenwälder
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
