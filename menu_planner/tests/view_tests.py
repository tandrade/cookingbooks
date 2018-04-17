from django.test import TestCase

from menu_planner.models import  IngestedRecipe

class RecipeCreateTests(TestCase):

    def test_create_recipe_saves_raw_response(self):
        mock_url = 'http://www.fakecooking.blog/recipe/1/'
        mock_content = '''
            <html>
            This is content to ingest.
            </html>
        '''
        self.assertEqual(IngestedRecipe.objects.count(), 0)
        response = self.client.post(reverse('recipe-list'), {
            'url': mock_url,
            'type': 'internet'
        })
        self.assertStatus(response, 200)
        self.assertEqual(IngestedRecipe.objects.count(), 1)

        saved = IngestedRecipe.objects.first()
        self.assertEqual(saved.url, mock_url)
        self.assertEqual(saved.content)

    def test_create_recipe_fails_with_unsupported_type(self):
        pass`


class RecipeGetTests(TestCase):

    def test_get_returns_all_recipes(self):
        pass
