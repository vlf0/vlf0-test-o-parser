from rest_framework import serializers
from .models import ParsedData


class CountSerializer(serializers.Serializer):

    count = serializers.IntegerField(default=10, max_value=50)


class ParsingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParsedData
        fields = ['name', 'price', 'description', 'image_url', 'discount']

