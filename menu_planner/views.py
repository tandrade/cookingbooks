from rest_framework import exceptions, viewsets

from menu_planner.models import IngestedRecipe
from menu_planner.parsers import InternetParser
from menu_planner.serializers import InternetRecipeSerializer


class IngestedRecipeViewset(viewsets.ModelViewSet):

    def get_serializer_class(self):
        doc_type = self.request.POST.get("source_type")
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


internet_parser = InternetParser()
