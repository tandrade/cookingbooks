from bs4 import BeautifulSoup
import os
import unittest

from django.test import TestCase

from menu_planner import models
from menu_planner.parsers import InternetParser
from menu_planner.models import (Recipe, Ingredient, RecipeIngredientItem)


class TestCarrotSaladParsing(TestCase):

    def setUp(self):
        self.parser = InternetParser()
        with open(os.path.join(os.path.join(os.path.dirname(__file__), "data"), "carrot_salad__community_table")) as f:
            content = BeautifulSoup("".join(f.readlines()), "html.parser")
            self.parser.parse(content)

    def test_basic_recipe_info(self):
        recipe_title = "Carrot Salad with Tahini, Chickpeas and Pistachios"
        cooking_time = 30
        self.assertEqual(self.parser.recipe_data['title'], recipe_title)
        self.assertEqual(self.parser.recipe_data['cooking_time'], {'minimum': cooking_time, 'maximum': cooking_time})

        self.assertEqual(models.Recipe.objects.count(), 1)
        generated_recipe = models.Recipe.objects.first()
        self.assertEqual(generated_recipe.name, recipe_title)
        self.assertEqual(generated_recipe.cooking_time_minutes, cooking_time)

    @unittest.skip("FIXME: implement object creation.")
    def test_creates_ingredients(self):
        self.assertEqual(len(self.parser.ingredients), 12)
        self.assertEqual(Ingredient.objects.count(), 12)

        all_names = (
            "chickpeas",
            "olive oil",
            "coarse sea salt",
            "ground cumin",
            "lemon juice",
            "tahini",
            "water",
            "minced", # Bad data
            "sea salt and red pepper flakes",
            "carrots",
            "coarsely chopped flat-leaf parsley",
            "salted pistachios"
        )
        self.assertEqual(list(all_names), [ingredient.name.lower() for ingredient in self.parser.ingredients])
        self.assertEqual(list([r.name for r in Recipe.objects.all()]), list(all_names))


        all_desc = (
            "drained and rinsed",
            "divided",
            "to taste",
            "peeled and coarsely grated",
            "coarsely chopped",
        )
        to_match_ingredients = [ingredient.desc.lower() for ingredient in self.parser.ingredients if ingredient.desc]
        self.assertEqual(list(all_desc), to_match_ingredients)
        self.assertEqual(RecipeIngredientItem.objects.count(), 12)

        # spot checking how recipe ingredient items are created
        ri1 = RecipeIngredientItem.objects.get(recipe_id__name="chickpeas")
        self.assertEqual(ri1.other_instructions, "drained and rinsed")

        ri2 = RecipeIngredientItem.objects.get(recipe_id__name="carrots")
        self.assertEqual(ri2.other_instructions, "peeled and coarsely grated")

        all_quantities = (
            '1 (15.5-oz) can',
            '3 tbsp',
            '½ tsp',
            '¼ tsp',
            '¼ cup',
            '3 tbsp',
            '2 tbsp',
            '1 garlic clove',
            '1 lb',
            '¼ cup',
            '¼ cup',
        )

        to_match_ingredients = [ingredient.quantity.lower() for ingredient in self.parser.ingredients if ingredient.quantity]
        self.assertEqual(list(all_quantities), to_match_ingredients)

    def test_creates_steps(self):
        pass
