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
    app.logger.info("num recommendations requested " + str(num))
    r = similarities.calc_simple_similarity(recipe_id, num)
    return r


def _ensure_num(num):
    if (num is None) or (int(num) < -1):
        num = -1
    return int(num)
