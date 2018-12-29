from django.test import TestCase

from menu_planner.models import Ingredient, Recipe
from menu_planner.serializers import IngredientSerializer, RecipeIngredientItemSerializer


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


class IngredientSerializerTest(TestCase):

    def test_different_capitalization(self):
        i1 = IngredientSerializer(data={"name": "onion"})
        self.assertTrue(i1.is_valid())
        i1.save()
        self.assertEqual(len(Ingredient.objects.all()), 1)

        i2 = IngredientSerializer(data={"name": "Onion"})
        self.assertTrue(i2.is_valid())
        i2.save()
        self.assertEqual(len(Ingredient.objects.all()), 1)

    def test_plurals_dont_create_multiple(self):
        i1 = IngredientSerializer(data={"name": "chickpea"})
        self.assertTrue(i1.is_valid())
        i1.save()
        self.assertEqual(len(Ingredient.objects.all()), 1)

        i2 = IngredientSerializer(data={"name": "chickpeas"})
        self.assertTrue(i2.is_valid())
        i2.save()
        self.assertEqual(len(Ingredient.objects.all()), 1)
