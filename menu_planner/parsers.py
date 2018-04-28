
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

    def get_ingredient_parser():
        raise NotImplementedError

    def parse(self, content):
        self.ingredient_parser = self.get_ingredient_parser()
        self.recipe_data['title'] = get_name(content)
        self.recipe_data['cooking_time']['maximum'], self.recipe_data['cooking_time']['minimum'] = get_cooking_times(content)
        self.recipe_data['serves']['maximum'], self.recipe_data['serves']['minimum'] = get_servings(content)

        raw_ingredients = parse_ingredients(content)
        for ingredient in raw_ingredients:
            self.ingredients.append(ingredient_parser(ingredient))
        self.steps = parse_steps(content)

    @staticmethod
    def get_name(content):
        raise NotImplementedError

    @staticmethod
    def get_servings(content):
        raise NotImplementedError

    @staticmethod
    def get_cooking_times(content):
        raise NotImplementedError

    @staticmethod
    def parse_cooking_time(content):
        raise NotImplementedError

    @staticmethod
    def parse_ingredients(content):
        raise NotImplementedError

    @staticmethod
    def parse_steps(content):
        raise NotImplementedError


class InternetIngredientParsers(IngredientListParser):
    pass


class InternetParser(Parser):

    def get_ingredient_parser(self):
        return InternetIngredientParsers

    def get_name(content):
        pass
