import httpretty
from django.test import TestCase
from django.urls import reverse
from unittest import mock

from menu_planner.models import  InternetRecipe, Recipe


class RecipeCreateTest(TestCase):

    def fake_ingestor(self, _args=None):
        return "This is content to ingest."

    def setUp(self):
        self.mock_url = "http://www.fakecooking.blog/recipe/1/"

    @httpretty.activate
    @mock.patch('menu_planner.parsers.InternetParser.parse', fake_ingestor)
    def test_create_recipe_saves_raw(self):
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

        saved = InternetRecipe.objects.first()
        self.assertEqual(saved.source, self.mock_url)
        self.assertEqual(saved.content, self.fake_ingestor())

    def test_create_recipe_fails_with_unsupported_type(self):
        self.assertEqual(InternetRecipe.objects.count(), 0)
        response = self.client.post(reverse("ingested-list"), {
            "source": self.mock_url,
            "source_type": "bad_type"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(InternetRecipe.objects.count(), 0)


class RecipeGetTest(TestCase):

    def test_get_returns_all_recipes(self):
        #TODO: implement me
        pass
