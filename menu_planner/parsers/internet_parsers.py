from .base import IngredientListParser, Parser
import re


class InternetIngredientParsers(IngredientListParser):

    def get_ingredient_name(self, content):
        full_name = content.findAll('span', {'class': 'name'})[0]
        text = full_name.getText()
        return text.split(",")[0]

    def get_ingredient_desc(self, content):
        full_name = content.findAll('span', {'class': 'name'})[0]
        text = full_name.getText()
        if len(text.split(",")) > 1:
            return "".join(text[text.index(",") + 1:]).strip()
        return None

    def get_quantity(self, content):
        desc = content.findAll('span', {'class': 'amount'})[0]
        return desc.getText().strip()


class InternetParser(Parser):

    def get_ingredient_parser(self):
        return InternetIngredientParsers

    def get_name(self, content):
        return content.title.string

    def get_cooking_times(self, content):
        time_value = content.find_all('time', {'class': 'totaltime'})[0].getText()
        total_time = self.parse_time_value(time_value)
        # right now if there's only one value set for a time, just repeat that time twice
        return total_time, total_time

    def get_servings(self, content):
        recipe_metadata = content.find_all('ul', {'class': 'recipe_meta'})[0]
        found_servings = False
        max_servings = 0
        min_servings = 0
        for li in recipe_metadata:
            if 'serves' in str(li).lower():
                for tag in li.findAll('p'):
                    raw_value = tag.getText()
                    min_servings, max_servings = self.parse_servings(raw_value)
        return min_servings, max_servings

    def parse_ingredients(self, content):
        return content.find_all('li', {'class': 'ingredient'})
