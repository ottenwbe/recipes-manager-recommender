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


from flask import Flask, jsonify
import logging
from analyzer.config import RecipeStatsConfig

RECIPE_CONFIG = None


def configure_app():
    global RECIPE_CONFIG
    logging.info("Configuring Recipes Analyzer...")
    RECIPE_CONFIG = RecipeStatsConfig()
    RECIPE_CONFIG.make_config()
    logging.info("Configuration complete.")


app = Flask("recipes-analyzer")

@app.route('/api/v1/recommendation/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify that the service is responding.
    """
    return jsonify({
        "status": "healthy"
    }), 200

# Run configuration
configure_app()

# import the controller
from analyzer import controller

app.logger.info("Recipes Analyzer started")
