# recipes-recommender

[![Build and Deploy App](https://github.com/ottenwbe/recipes-manager-recommender/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/ottenwbe/recipes-manager-recommender/actions/workflows/python-package.yml)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ottenwbe/recipes-manager-recommender/blob/master/LICENSE)

Micro-Service that analyzes the recipes of [recipes-manager](https://github.com/ottenwbe/recipes-manager).

## Features

1. Recommend recipes based on similarities of components

    ````
    <url>/api/v1/recommendation/<recipe_id>/components
    ````


## Run with Flask

1. Install Dependencies

    ````bash
    pip install -r requirements.txt
    ````

2. Start Application

    ````bash
    FLASK_DEBUG=1 FLASK_APP="analyzer" flask run
    ````

## Development

### Testing

1. Install Test Dependencies (includes production requirements):
    ````bash
    pip install -r requirements-test.txt
    ````

2. Run the test suite:
    ````bash
    pytest -v
    ````

### Code Formatting

This project uses **Black** for code formatting. To format your code before committing, run:

````bash
black .
````

## Release

GitHub Workflows are used for testing and also building releases of docker containers.

To create a version, simply tag the master branch.

````bash
git tag v<next release>
git push --tags
````