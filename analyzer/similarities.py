# Copyright (c) 2021 Beate Ottenwälder
# SPDX-License-Identifier: MIT


import logging
from analyzer import recipes_client


def calc_simple_similarity(recipe_id, num, c=None):
    """Calculate similarities of other recipes based on given id"""
    if c is None:
        c = recipes_client.Client()

    recipes = c.get_full_recipes()
    component_per_recipe = _extract_recipe_components(recipes)
    recipe_similarities = _calc_jaccard_similarities(
        component_per_recipe[recipe_id], component_per_recipe
    )
    recipe_similarities = _sort_and_crop(recipe_similarities, num)

    return {"recipes": _make_result(recipe_similarities)}


def _make_result(similarities):
    result = []
    for s in similarities:
        result.append(s["id"])
    return result


def _jaccard_similarity_set(set1, set2):
    intersection = len(set1 & set2)
    union = (len(set1) + len(set2)) - intersection
    if union > 0:
        return intersection / union
    else:
        return 0.0


def _take_score(element):
    return element["score"]


def _sort_and_crop(scores, num):
    scores.sort(key=_take_score, reverse=True)
    if num >= 0:
        return scores[:num]
    return scores


def _calc_jaccard_similarities(reference_recipe, component_per_recipe):
    recipe_similarities = []
    for val in component_per_recipe.values():
        recipe_similarities = _append_recipe_similarity(
            reference_recipe, recipe_similarities, val
        )
    logging.debug(f"Calculated similarities: {recipe_similarities}")
    return recipe_similarities


def _append_recipe_similarity(reference_recipe, recipe_similarities, val):
    if reference_recipe["id"] != val["id"]:
        score = _jaccard_similarity_set(
            reference_recipe["components"], val["components"]
        )
        recipe_similarities.append({"id": val["id"], "score": score})
    return recipe_similarities


def _extract_recipe_components(recipes):

    component_per_recipe = dict()

    for r in recipes:
        components = set()
        try:
            for component in r["components"]:
                components.add(component["name"])

            recipe_id = str(r["id"])
            component_per_recipe[recipe_id] = {
                "id": recipe_id,
                "components": components,
            }
        except (KeyError, TypeError) as e:
            logging.error(f"Could not add valid recipe due to missing data: {e}")

    logging.debug(component_per_recipe)
    return component_per_recipe
