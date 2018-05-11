
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
        # self.recipe_data['cooking_time']['maximum'], self.recipe_data['cooking_time']['minimum'] = self.get_cooking_times(content)
        # self.recipe_data['serves']['maximum'], self.recipe_data['serves']['minimum'] = self.get_servings(content)
        #
        # raw_ingredients = parse_ingredients(content)
        # for ingredient in raw_ingredients:
        #     self.ingredients.append(ingredient_parser(ingredient))
        # self.steps = parse_steps(content)

    def get_name(self, content):
        raise NotImplementedError

    def get_servings(self, content):
        raise NotImplementedError

    def get_cooking_times(self, content):
        raise NotImplementedError

    def parse_cooking_time(self, content):
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
