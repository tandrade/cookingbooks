class IngredientQuantityParserMixin():

    def numeric_value(self, to_parse):
        if "/" in to_parse:
            potential_fractions = to_parse.split("/")
            if len(potential_fractions) != 2:
                return None
            try:
                numerator = float(potential_fractions[0])
                denominator = float(potential_fractions[1])
                return numerator / denominator
            except ValueError:
                return None
        try:
            return float(to_parse)
        except ValueError:
            return None

    recognized_units = [
        'oz',
        'ounce'
        'ounces',
        'tbsp',
        'tablespoon',
        'tsp',
        'teaspoon',
        'cup',
        'quart',
        'lb',
        'pound',
    ]

    def parse_quantity(self, txt):
        removable_chars = ["(", ")", "."]
        cleaned = txt
        for char in removable_chars:
            cleaned = txt.replace(char, "")
        words = txt.split(" ")
        for index, word in enumerate(words[:-1]):
            numeric_value = self.numeric_value(word)
            following = self.numeric_value(words[index + 1])
            if numeric_value and not following:
                # we've found a numeric value followed by a string
                return (numeric_value, words[index+1])
        return None, None
