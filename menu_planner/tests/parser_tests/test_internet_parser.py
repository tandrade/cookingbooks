from bs4 import BeautifulSoup
import os
import unittest

from django.test import TestCase

from menu_planner.parsers import InternetParser


class TestInternetParser(TestCase):

    def setUp(self):
        self.parser = InternetParser()
        with open(os.path.join(os.path.join(os.path.dirname(__file__), "data"), "carrot_salad__community_table")) as f:
            content = BeautifulSoup("".join(f.readlines()), "html.parser")
            self.parser.parse(content)

    def test_basic_recipe_info(self):
        self.assertEqual(self.parser.recipe_data['title'], "Carrot Salad with Tahini, Chickpeas and Pistachios")

    @unittest.skip("Redundant errors for now.")
    def test_creates_steps(self):
        pass

    @unittest.skip("Redundant errors for now.")
    def test_creates_ingredients(self):
        pass
