from rest_framework import serializers
from menu_planner import models


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
        instance, _created = models.Ingredient.objects.get_or_create(**validated_data)
        return instance


class RecipeIngredientItemSerializer(serializers.ModelSerializer):

    denomination = serializers.SerializerMethodField()

    class Meta:
        model = models.RecipeIngredientItem
        fields = ['recipe_id', 'ingredient_id', 'other_instructions', 'optional', 'amount', 'denomination']
        extra_kwargs = {
            'recipe_id': {'write_only': True},
            'ingredient_id': {'write_only': True}
        }

    def get_denomination(self, obj):
        # FIXME: is there a better way to accomplish this?
        return obj.denomiation.replace('.', '').lower() if obj.denomination else None
