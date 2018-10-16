import httpretty
from django.test import TestCase
from django.urls import reverse
from unittest import mock, skip

from menu_planner.models import (Ingredient,
                                 InternetRecipe,
                                 Recipe)


class RecipeCreateTest(TestCase):

    def fake_parser(self, _args=None):
        return "This is content to ingest."

    def setUp(self):
        self.mock_url = "http://www.fakecooking.blog/recipe/1/"

    @httpretty.activate
    @mock.patch('menu_planner.parsers.InternetParser.parse', fake_parser)
    @mock.patch('django.db.models.signals.post_save.send')
    def test_create_recipe_saves_raw(self, signals_mock):
        mock_content = '''
            <html>
            This is content to ingest.
            </html>
        '''
        httpretty.register_uri(httpretty.GET,
                              self.mock_url,
                              body=mock_content)
        self.assertEqual(InternetRecipe.objects.count(), 0)
        response = self.client.post(reverse("ingested-list"), {
            "source": self.mock_url,
            "source_type": "internet"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(InternetRecipe.objects.count(), 1)
        assert signals_mock.called
        saved = InternetRecipe.objects.first()
        self.assertEqual(saved.source, self.mock_url)
        self.assertEqual(saved.content, self.fake_parser())

    def test_create_recipe_fails_with_unsupported_type(self):
        self.assertEqual(InternetRecipe.objects.count(), 0)
        response = self.client.post(reverse("ingested-list"), {
            "source": self.mock_url,
            "source_type": "bad_type"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(InternetRecipe.objects.count(), 0)


class RecipeViewTest(TestCase):

    def setUp(self):
        for ingredient in ["chickpeas", "carrots", "cumin"]:
            Ingredient.objects.create(name=ingredient.lower())
        Recipe.objects.create(name="Cool Recipe")

    def test_get_returns_all_recipes(self):
        results = self.client.get(reverse("recipe-list"))
        self.assertEqual(results.status_code, 200)

    def test_get_recipe(self):
        r = Recipe.objects.first()
        results = self.client.get(reverse("recipe-detail", args=[r.id]))
        self.assertEqual(results.status_code, 200)

    def test_post_not_allowed(self):
        results = self.client.post(reverse("recipe-list"), data={
            'title': 'Even Cooler Recipe'
        })
        self.assertEqual(results.status_code, 405)

    def test_update_fails(self):
        r = Recipe.objects.first()
        results = self.client.patch(reverse("recipe-detail", args=[r.id]))
        self.assertEqual(results.status_code, 405)

    @skip("Not implemented yet.")
    def test_filter_by_ingredient(self):
        for ingredient in ["parsley", "apples", "spinach"]:
            Ingredient.objects.create(name=ingredient.lower())
        Recipe.objects.create(name="Different Recipe")
        results = self.client.get(reverse("recipe-list"), {'ingredient': 'chickpeas'})
        self.assertEqual(results.status_code, 200)
        self.assertEqual(len(results.data), 1)
        self.assertEqual(results.data[0].title, "Cool Recipe")

    @skip("Not implemented yet.")
    def test_advanced_filter_by_ingredient(self):
        for ingredient in ["parsley", "apples", "spinach"]:
            Ingredient.objects.create(name=ingredient.lower())
        Recipe.objects.create(name="Different Recipe")
        results = self.client.get(reverse("recipe-list"), {'ingredient': ['chickpeas', 'apples']})
        self.assertEqual(results.status_code, 200)
        self.assertEqual(len(results.data), 0)
