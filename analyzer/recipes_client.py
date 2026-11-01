# Copyright (c) 2021 Beate Ottenwälder
# SPDX-License-Identifier: MIT

from threading import Lock
from time import monotonic

import requests

from analyzer import RECIPE_CONFIG, app

RECIPE_CACHE_TTL_SECONDS = 60
REQUEST_TIMEOUT_SECONDS = 5


class Client:
    def __init__(self, cache_ttl=RECIPE_CACHE_TTL_SECONDS):
        self._cache_ttl = cache_ttl
        self._recipes_cache = None
        self._cache_expires_at = 0
        self._cache_lock = Lock()

    def get_recipes(self):
        """Get a list (of ids) containing all recipes"""
        url = f"{RECIPE_CONFIG.RECIPE_SERVER}/api/v1/recipes"
        recipes, ok = self._get_json(url)
        if not ok:
            return {"recipes": []}
        return recipes

    def get_recipe(self, recipe_id):
        """Get a recipe by id"""
        url = f"{RECIPE_CONFIG.RECIPE_SERVER}/api/v1/recipes/r/{recipe_id}"
        recipe, ok = self._get_json(url)
        if not ok:
            return None
        return recipe

    def get_full_recipes(self):
        with self._cache_lock:
            if self._has_fresh_cache():
                return list(self._recipes_cache)

        recipes, ok = self._fetch_full_recipes()

        with self._cache_lock:
            if ok:
                self._recipes_cache = recipes
                self._cache_expires_at = monotonic() + self._cache_ttl
        return recipes

    def _has_fresh_cache(self):
        return self._recipes_cache is not None and monotonic() < self._cache_expires_at

    def clear_cache(self):
        with self._cache_lock:
            self._recipes_cache = None
            self._cache_expires_at = 0

    def _fetch_full_recipes(self):
        recipes = []

        url = f"{RECIPE_CONFIG.RECIPE_SERVER}/api/v1/recipes"
        recipe_ids, ok = self._get_json(url)
        if not ok:
            return recipes, False

        for recipe_id in recipe_ids["recipes"]:
            url = f"{RECIPE_CONFIG.RECIPE_SERVER}/api/v1/recipes/r/{recipe_id}"
            recipe, ok = self._get_json(url)
            if not ok:
                return recipes, False
            if recipe is not None:
                recipes.append(recipe)

        return recipes, True

    def _get_json(self, url):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request failed: {e} - {url}")
            return None, False
        if not response.ok:
            app.logger.error(
                f"Request failed: {response.status_code} - {url} - {response.text}"
            )
            return None, False
        return response.json(), True


DEFAULT_CLIENT = Client()
