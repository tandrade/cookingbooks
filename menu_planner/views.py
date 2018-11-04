from rest_framework import exceptions, mixins, viewsets

from menu_planner.models import Recipe
from menu_planner.parsers import InternetParser
from menu_planner.serializers import InternetRecipeSerializer, RecipeSerializer


class IngestedRecipeViewset(viewsets.ModelViewSet):

    def get_serializer_class(self):
        doc_type = self.request.data.get("source_type")
        if doc_type == "internet":
            return InternetRecipeSerializer
        raise exceptions.ValidationError("That source type is not supported.")

    def perform_create(self, serializer):
        content = None
        if serializer.validated_data["source_type"] == "internet":
            content = internet_parser.parse(serializer.validated_data["source"])
        serializer.save(content=content)

    @staticmethod
    def get_parser(data_type):
        if data_type == "internet":
            return internet_parser
        raise NotImplementedError



class RecipeViewset(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = RecipeSerializer

    def get_queryset(self):
        ingredients = self.request.query_params.getlist('ingredient')
        if not ingredients:
            return Recipe.objects.all()
        return Recipe.objects.filter(ingredient_items__ingredient_id__name__in=[
                 ingredient.lower() for ingredient in ingredients
                ])


internet_parser = InternetParser()
