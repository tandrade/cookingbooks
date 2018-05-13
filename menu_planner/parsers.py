import re


class IngredientListParser(object):

    def __init__(self, item):
        self.name = get_ingredient_name(item)
        self.quantity = get_quantity(item)

    def get_ingredient_name(object):
        raise NotImplementedError

    def get_quantity(object):
        raise NotImplementedError


class Parser(object):

    def __init__(self):
        self.recipe_data = {}
        self.ingredients = []
        self.steps = []

    def get_ingredient_parser(self):
        raise NotImplementedError

    def parse(self, content):
        self.ingredient_parser = self.get_ingredient_parser()
        self.recipe_data['title'] = self.get_name(content)
        # TODO: implement each of these steps
        maximum_time, minimum_time = self.get_cooking_times(content)
        self.recipe_data['cooking_time'] = {
            'maximum': maximum_time,
            'minimum': minimum_time
        }
        maximum_servings, minimum_servings = self.get_servings(content)
        self.recipe_data['servers'] = {
            'maximum': maximum_servings,
            'minimum': minimum_servings
        }

        #
        # raw_ingredients = parse_ingredients(content)
        # for ingredient in raw_ingredients:
        #     self.ingredients.append(ingredient_parser(ingredient))
        # self.steps = parse_steps(content)

    def parse_time_value(self, to_convert):
        all_values = to_convert.split(" ")
        total_time = 0
        contains_hours = False
        contains_minutes = False
        minute_values = None
        for value in all_values[::-1]:
            if 'min' in value:
                contains_minutes = True
            if 'hour' in value:
                contains_hours = True
            if contains_hours and value.isdigit():
                total_time += int(value) * 60
                contains_hours = False
            if contains_minutes and value.isdigit():
                total_time += int(value)
                contains_minutes = False
        return total_time

    def parse_servings(self, to_convert):
        all_values = to_convert.split('-')
        if len(all_values) == 1:
            all_values += all_values[0]
        return int(all_values[0]), int(all_values[1])

    def get_name(self, content):
        raise NotImplementedError

    def get_cooking_times(self, content):
        raise NotImplementedError

    def get_servings(self, content):
        raise NotImplementedError

    def parse_ingredients(self, content):
        raise NotImplementedError

    def parse_steps(self, content):
        raise NotImplementedError


class InternetIngredientParsers(IngredientListParser):
    pass


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
