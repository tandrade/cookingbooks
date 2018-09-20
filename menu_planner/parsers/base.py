from menu_planner import models

class IngredientListParser(object):

    def __init__(self, item):
        self.name = self.get_ingredient_name(item)
        self.desc = self.get_ingredient_desc(item)
        self.quantity = self.get_quantity(item)

    def get_ingredient_name(self, content):
        raise NotImplementedError

    def get_ingredient_desc(self, content):
        raise NotImplementedError

    def get_quantity(self, content):
        raise NotImplementedError


class Parser(object):
    '''
    Parses a recipe object, and creates database objects based on parsing result.
    In the event of this taking a long period of time, this could be split into an async
    job but for now it is a synchronous operation.
    '''

    def __init__(self):
        self.recipe_data = {}
        self.ingredients = []
        self.steps = []

    def get_ingredient_parser(self):
        raise NotImplementedError

    def create_recipe(self):
        return models.Recipe.objects.create(
            name=self.recipe_data['title'],
            cooking_time_minutes=self.recipe_data['cooking_time']['maximum'], # maybe average?
            serve_min=self.recipe_data['servers']['minimum'],
            serve_max=self.recipe_data['servers']['maximum']
        )

    def parse(self, content):
        # first, parse metadata related to this recipe
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

        recipe = self.create_recipe()

        # second, parse ingredients
        raw_ingredients = self.parse_ingredients(content)
        for ingredient in raw_ingredients:
            self.ingredients.append(self.ingredient_parser(ingredient))
        self.get_or_create_ingredients()

        # lastly, parse the recipe instructions
        # FIXME: implement this -- for now, not the most important part.
        # self.steps = self.parse_steps(content)

    def get_or_create_ingredients(self):
        pass

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
