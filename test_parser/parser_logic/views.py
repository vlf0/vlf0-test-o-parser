from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .tasks import parse
from .serializers import ParsingSerializer, CountSerializer
from .models import ParsedData


class ParserRunnerViewSet(viewsets.ViewSet):

    http_method_names = ['post']

    def create(self, request):
        serializer = CountSerializer(data=request.data)
        if serializer.is_valid():
            product_amount = serializer.data['count']
            parse.delay(product_amount)
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


class ParsedDataViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = ParsingSerializer
    queryset = ParsedData.objects.all()
