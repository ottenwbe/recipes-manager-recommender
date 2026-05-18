# Copyright (c) 2021 Beate Ottenwälder
# SPDX-License-Identifier: MIT


import logging
from flask import request
from analyzer import app, similarities


@app.route("/")
def root():
    """Root Route"""
    return "Recipes Analyzer"


@app.route("/api/v1/recommendation/<recipe_id>/components")
def recommend_recipe(recipe_id):
    """Recommend n recipes based on a recipe id.
    Example: <url>/api/v1/recommendation/1234/components?num=10
    """
    num = request.args.get("num")
    num = _ensure_num(num)
    app.logger.info(f"num recommendations requested: {num}")
    r = similarities.calc_simple_similarity(recipe_id, num)
    return r


def _ensure_num(num):
    try:
        if (num is None) or (int(num) < -1):
            return -1
        return int(num)
    except (ValueError, TypeError):
        return -1
