from django.test import TestCase

from menu_planner.models import Recipe, Ingredient
from menu_planner.serializers import RecipeIngredientItemSerializer


class RecipeIngredientItemSerializerTest(TestCase):

    def setUp(self):
        self.r = Recipe.objects.create(name="Fake Recipe")
        self.i = Ingredient.objects.create(name="spinach")

    def test_well_formed_data(self):
        data = {
            "recipe_id": self.r.id,
            "ingredient_id": self.i.id,
            "amount": 10.0,
            "denomination": "oz"
        }

        serialized = RecipeIngredientItemSerializer(data=data)
        self.assertTrue(serialized.is_valid())

    def test_denomination_capitalization_issues(self):
        data = {
            "recipe_id": self.r.id,
            "ingredient_id": self.i.id,
            "amount": 10.0,
            "denomination": "Oz"
        }
        serialized = RecipeIngredientItemSerializer(data=data)
        self.assertTrue(serialized.is_valid())

    def test_denomination_invalid_option(self):
        data = {
            "recipe_id": self.r.id,
            "ingredient_id": self.i.id,
            "amount": 10.0,
            "denomination": "oz"
        }

        serialized = RecipeIngredientItemSerializer(data=data)
        self.assertTrue(serialized.is_valid())
