# Copyright (c) 2021 Beate Ottenwälder
# SPDX-License-Identifier: MIT

import requests

from analyzer import RECIPE_CONFIG, app


class Client:
    def get_recipes(self):
        """Get a list (of ids) containing all recipes"""
        # Using f-strings for better readability
        url = f"{RECIPE_CONFIG.RECIPE_SERVER}/api/v1/recipes"
        r = requests.get(url)
        if not r.ok:
            self._log_error(url, r)
            return {"recipes": []}
        return r.json()

    def get_recipe(self, recipe_id):
        """Get a recipe by id"""
        url = f"{RECIPE_CONFIG.RECIPE_SERVER}/api/v1/recipes/r/{recipe_id}"
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
            f"Request failed: {r.status_code} - {url} - {r.text}"
        )
