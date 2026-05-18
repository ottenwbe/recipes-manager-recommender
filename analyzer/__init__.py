# Copyright (c) 2021 Beate Ottenwälder
# SPDX-License-Identifier: MIT


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


@app.route("/api/v1/recommendation/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify that the service is responding.
    """
    return jsonify({"status": "healthy"}), 200


# Run configuration
configure_app()

# import the controller
from analyzer import controller

app.logger.info("Recipes Analyzer started")
