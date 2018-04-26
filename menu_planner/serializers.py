from ingestors import InternetIngestor


class IngestedRecipeSerializer(viewsets.Seralizer):
    content = serializer.MethodSerializer()
    external_link = serializer.TextField()
    recipe_type = serializer.TextField()

    @staticmethod
    def get_ingestor_class(obj):
        if obj.type == 'url':
            return InternetIngestor
        raise NotYetImplemented

    def get_content(self, obj):
        ingestor = self.get_ingestor_class(obj)
        return ingestor.ingest(obj.external_link)
