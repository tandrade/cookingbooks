from rest_framework import viewsets

from menu_planner.models import IngestedRecipe


class IngestedRecipeViewset(viewsets.ModelViewSet):

    @staticmethod
    def get_parser(data_type):
        if data_type == 'internet':
            return InternetParser
        raise NotYetImplemented

    def create(self, request, *args, **kwargs):
        if 'type' not in args:
            raise ValidationError("Type of recipe to create must be specified.")
        if args["type"] != "url":
            raise ValidationError("Only ingestion from URL is supported at this time.")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        parser = self.get_parser(serializer.data['type'])
        # for now (simplest case), don't catch errors and don't save serializer if parsing fails
        # FIXME: eventually this will be moved to an async job and the failures will be separted that way
        parser.parse(serializer.content)
        serializer.save()
