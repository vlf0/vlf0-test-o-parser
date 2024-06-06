from rest_framework import serializers
from .models import ParsedData


class CountSerializer(serializers.Serializer):

    count = serializers.IntegerField(default=10, max_value=50)


class BaseParsingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParsedData
        fields = ['name', 'price', 'description', 'image_url', 'discount', 'link']


class ParsingSerializer(BaseParsingSerializer):

    class Meta(BaseParsingSerializer.Meta):
        fields = ['name', 'price', 'description', 'image_url', 'discount']


class ParsingSerializerLink(BaseParsingSerializer):

    class Meta(BaseParsingSerializer.Meta):
        fields = ['name', 'link']