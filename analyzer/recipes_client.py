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

import requests

from analyzer import RECIPE_CONFIG, app


class Client:

    def __init__(self):
        pass

    def get_recipes(self):
        """Get a list (of ids) containing all recipes"""
        url = "{}/api/v1/recipes".format(RECIPE_CONFIG.RECIPE_SERVER)
        r = requests.get(url)
        if not r.ok:
            self._log_error(url, r)
            return {"recipes": []}
        return r.json()

    def get_recipe(self, recipe_id):
        """Get a recipe by id"""
        url = "{}/api/v1/recipes/r/{}".format(RECIPE_CONFIG.RECIPE_SERVER, recipe_id)
        r = requests.get(url)
        if not r.ok:
            self._log_error(url, r)
            return None
        return r.json()

    def get_full_recipes(self):
        recipes = []

        recipe_ids = self.get_recipes()
        for recipe_id in recipe_ids["recipes"]:
            r = self.get_recipe(recipe_id)
            if r is not None:
                recipes.append(r)

        return recipes

    def _log_error(self, url, r):
        app.logger.error(
            "Reqeuest failed: {} - {} - {}".format(r.status_code, url, r.text)
        )
