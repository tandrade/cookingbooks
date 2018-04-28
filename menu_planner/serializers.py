from rest_framework import serializers
from menu_planner.ingestors import InternetIngestor


class IngestedRecipeSerializer(serializers.ModelSeralizer):
    content = serializers.MethodSerializer()
    
    class Meta:
        fields = ['external_ref', 'content', 'source']

    @staticmethod
    def get_ingestor_class(obj):
        if obj.type == "url":
            return InternetIngestor
        raise NotImplementedError

    def get_content(self, obj):
        ingestor = self.get_ingestor_class(obj)
        return ingestor.ingest(obj.external_link)
