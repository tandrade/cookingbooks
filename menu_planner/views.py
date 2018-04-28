from django.core.exceptions import ValidationError
from rest_framework import viewsets

from menu_planner.models import IngestedRecipe
from menu_planner.parsers import InternetParser
from menu_planner.serializers import IngestedRecipeSerializer


class IngestedRecipeViewset(viewsets.ModelViewSet):

    serializer_class = IngestedRecipeSerializer

    @staticmethod
    def get_parser(data_type):
        if data_type == "url":
            return InternetParser
        raise NotImplementedError

    def create(self, request, *args, **kwargs):
        doc_type = self.request.POST.get("type")
        if not doc_type:
            raise ValidationError("Type of recipe to create must be specified.")
        if doc_type != "url":
            raise ValidationError("Only ingestion from URL is supported at this time.")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        parser = self.get_parser(serializer.data["recipe_type"])
        # for now (simplest case), don't catch errors and don't save serializer if parsing fails
        # FIXME: eventually this will be moved to an async job and the failures will be separted that way
        parser.parse(serializer.content)
        serializer.save()
