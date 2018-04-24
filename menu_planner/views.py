from rest_framework import viewsets

from menu_planner.models import IngestedRecipe


class IngestedRecipeViewset(viewsets.ModelViewSet):

    queryset = IngestedRecipe.objects.all()


class RecipeViewset(viewsets.ModelViewSet):
    pass
