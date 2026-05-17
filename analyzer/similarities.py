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
from analyzer import recipes_client


def calc_simple_similarity(recipe_id, num, c=recipes_client.Client()):
    """Calculate similarities of other recipes based on given id"""
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
    intersection = len(list(set1.intersection(set2)))
    union = (len(set1) + len(set2)) - intersection
    if union > 0:
        return float(intersection) / union
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
    logging.error(recipe_similarities)
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
        except:
            logging.error("Could not add valid recipe")

    logging.debug(component_per_recipe)
    return component_per_recipe
