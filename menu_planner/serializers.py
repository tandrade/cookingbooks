from rest_framework import serializers
from menu_planner.models import InternetRecipe


class InternetRecipeSerializer(serializers.ModelSerializer):

    content = serializers.ReadOnlyField()

    class Meta:
        model = InternetRecipe
        fields = ['source_type', 'content', 'source']
