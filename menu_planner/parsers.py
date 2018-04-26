
class IngredientListParser(object):

    def __init__(self, item):
        self.name = get_ingredient_name(item)
        self.quantity = get_quantity(item)

    def get_ingredient_name(object):
        pass

    def get_quantity(object):
        pass


class Parser(object):

    def get_ingredient_parser():
    raise NotImplentedException

    @transaction.atomic
    def parse(self, content):
        self.ingredient_parser = self.get_ingredient_parser()
        self.title = get_name(content)
        self.cooking_time = get_cooking_times(content)
        self.minimum_served, self.maximum_served = parse_cooking_time(content)
        
        ingredients = parse_ingredients(content)
        for ingredient in ingredients:
            ingredient_parser(ingredient)
        self.steps = parse_steps(content)

    @staticmethod
    def get_name(content):
        raise NotImplentedException

    @staticmethod
    def get_cooking_times(content):
        raise NotImplentedException

    @staticmethod
    def parse_cooking_time(content):
        raise NotImplentedException

    @staticmethod
    def parse_ingredients(content):
        raise NotImplentedException

    @staticmethod
    def parse_steps(content):
        raise NotImplentedException


class InternetParsers(Parser):

    def get_name(content):
        pass
