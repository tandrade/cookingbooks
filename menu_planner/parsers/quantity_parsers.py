class IngredientQuantityParserMixin():

    unicode_matches = {
        "\u00BD": 0.5,
        "\u2189": 0.0,
        "\u2152": 0.1,
        "\u2152": 0.1,
        "\u2151": 0.111,
        "\u215B": 0.125,
        "\u2150": 0.142,
        "\u2159": 0.167,
        "\u2155": 0.2,
        "\u00BC": 0.25,
        "\u2153": 0.333,
        "\u215C": 0.375,
        "\u2156": 0.4,
        "\u00BD": 0.5,
        "\u2157": 0.6,
        "\u215D": 0.625,
        "\u2154": 0.667,
        "\u00BE": 0.75,
        "\u2158": 0.8,
        "\u215A": 0.833,
        "\u215E": 0.875,
    }

    def numeric_value(self, to_parse):
        unicode_match = self.unicode_matches.get(to_parse)
        if unicode_match:
            return unicode_match
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
        'to taste'
    ]

    def parse_quantity(self, txt):
        removable_chars = ["(", ")"]
        spaced_chars = ["-"]
        cleaned = txt
        if txt.lower() == 'to taste':
            return 0.01, "tsp"
        for char in removable_chars:
            cleaned = cleaned.replace(char, "")
        for char in spaced_chars:
            cleaned = cleaned.replace(char, " ")
        words = cleaned.split(" ")
        for index, word in enumerate(words[:-1]):
            numeric_value = self.numeric_value(word)
            following = self.numeric_value(words[index + 1])
            if numeric_value and not following:
                # we've found a numeric value followed by a string
                return (numeric_value, words[index+1])
        return None, None
