from rest_framework import serializers
from menu_planner.models import InternetRecipe, Recipe


class InternetRecipeSerializer(serializers.ModelSerializer):

    content = serializers.ReadOnlyField()

    class Meta:
        model = InternetRecipe
        fields = ['source_type', 'content', 'source']



class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['name',]
