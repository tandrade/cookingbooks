from rest_framework import serializers
from menu_planner import models
from nltk.stem.porter import PorterStemmer


stemmer = PorterStemmer()


class InternetRecipeSerializer(serializers.ModelSerializer):

    content = serializers.ReadOnlyField()

    class Meta:
        model = models.InternetRecipe
        fields = ['source_type', 'content', 'source']


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipe
        fields = ['name',]


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = ['name']

    def validate_name(self, name):
        # TODO: handle plurals
        return name.lower()

    def create(self, validated_data):
        normalized_name = stemmer.stem(validated_data['name'])
        try:
            instance = models.Ingredient.objects.get(normalized_name=normalized_name)
            return instance
        except models.Ingredient.DoesNotExist:
            pass  # expected error
        # technically there is a race condition here because this create operation is not in the same
        # transaction as the get. in reality, this app will be too low traffic for this race condition to
        # occur 
        created = models.Ingredient.objects.create(name=validated_data['name'], normalized_name=normalized_name)
        return created


class DenominationField(serializers.CharField):

    denominations = {
        models.RecipeIngredientItem.TEASPOON: ('teaspoon', 'teaspoons', 'tsp', 'tsps'),
        models.RecipeIngredientItem.TABLESPOON: ('tablespoon', 'tablespoons', 'tbsp', 'tbsps'),
        models.RecipeIngredientItem.GRAM: ('gram', 'grams', 'g', 'gs'),
        models.RecipeIngredientItem.CUP: ('cup', 'cups', ),
        models.RecipeIngredientItem.QUART: ('quart', 'quarts', 'qt', 'qts', ),
        models.RecipeIngredientItem.OUNCE: ('ounce', 'ounces', 'oz', 'ozs',),
        models.RecipeIngredientItem.POUND: ('pound', 'pounds', 'lb', 'lbs',),
    }

    value_measurements = {measurement: key for key, values in denominations.items() for measurement in values}

    def get_value(self, data):
        if 'denomination' in data:
            value = self.value_measurements.get(data['denomination'].lower())
            if value:
                return value
        # sometimes, bad data gets through -- just give it a count
        return models.RecipeIngredientItem.COUNT


class RecipeIngredientItemSerializer(serializers.ModelSerializer):

    denomination = DenominationField()

    class Meta:
        model = models.RecipeIngredientItem
        fields = ['recipe_id', 'ingredient_id', 'other_instructions', 'optional', 'amount', 'denomination']
        extra_kwargs = {
            'recipe_id': {'write_only': True},
            'ingredient_id': {'write_only': True}
        }

    def to_internal_value(self, data):
        if not data['amount'] and not data['denomination'] and data['other_instructions'] and data['other_instructions'].lower().strip() == 'to taste':
            data['amount'] = 0.001
            data['denomination'] = models.RecipeIngredientItem.TEASPOON
        return super().to_internal_value(data)
