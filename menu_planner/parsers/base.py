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


        raw_ingredients = self.parse_ingredients(content)
        for ingredient in raw_ingredients:
            self.ingredients.append(self.ingredient_parser(ingredient))
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
