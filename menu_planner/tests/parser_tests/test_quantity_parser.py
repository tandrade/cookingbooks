from django.test import TestCase

from menu_planner.parsers import IngredientQuantityParserMixin


class IngredientQuantityParserTest(TestCase):

    def test_recognize_basic_measurements(self):
        num, denom = IngredientQuantityParserMixin().parse_quantity("16 oz.")
        self.assertEqual(num, 16)
        self.assertEqual(denom, "oz.")

    def test_unicode_percentages(self):
        num, denom = IngredientQuantityParserMixin().parse_quantity("½ tsp")
        self.assertEqual(num, 0.5)
        self.assertEqual(denom, "tsp")

    def test_recognize_parentheticals(self):
        # TODO: implement me
        num, denom = IngredientQuantityParserMixin().parse_quantity("1 (15.5 oz) can")
        self.assertEqual(num, 15.5)
        self.assertEqual(denom, "oz")

    def test_handle_hyphens(self):
        num, denom = IngredientQuantityParserMixin().parse_quantity("7-oz. can")
        self.assertEqual(num, 7)
        self.assertEqual(denom, "oz.")
