from django.test import TestCase
from django.urls import reverse

from menu_planner.models import  IngestedRecipe, Recipe

class RecipeCreateTest(TestCase):

    def setUp(self):
        self.mock_url = "http://www.fakecooking.blog/recipe/1/"

    def test_create_recipe_saves_raw(self):
        mock_content = '''
            <html>
            This is content to ingest.
            </html>
        '''
        self.assertEqual(IngestedRecipe.objects.count(), 0)
        response = self.client.post(reverse("ingested-list"), {
            "url": self.mock_url,
            "type": "internet"
        })
        self.assertStatus(response, 200)
        self.assertEqual(IngestedRecipe.objects.count(), 1)

        saved = IngestedRecipe.objects.first()
        self.assertEqual(saved.url, mock_url)
        self.assertEqual(saved.content)

    def test_create_recipe_fails_with_unsupported_type(self):
        self.assertEqual(IngestedRecipe.objects.count(), 0)
        response = self.client.post(reverse("ingested-list"), {
            "url": self.mock_url,
            "type": "bad_type"
        })
        self.assertStatus(response, 400)
        self.assertEqual(IngestedRecipe.objects.count(), 0)


class RecipeGetTest(TestCase):

    def test_get_returns_all_recipes(self):
        #TODO: implement me
        pass
