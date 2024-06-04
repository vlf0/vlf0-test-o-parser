from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import ParsingSerializer, CountSerializer
from .models import ParsedData
from .tasks_manager import TasksManager

task_manager = TasksManager()


class ParserRunnerViewSet(viewsets.ViewSet):

    http_method_names = ['post']

    @swagger_auto_schema(operation_summary='run parsing task',
                         responses={200: 'Parser starting success', 400: 'Invalid input'},
                         query_serializer=CountSerializer)
    def create(self, request):
        task_manager.request = request
        if task_manager.parser_task():
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


class ParsedDataViewSet(viewsets.ModelViewSet):

    http_method_names = ['get']
    serializer_class = ParsingSerializer
    user_response = openapi.Response('response description', ParsingSerializer)

    @swagger_auto_schema(operation_summary='get one of parsed products by ID',
                         responses={200: user_response, 500: 'Server error'})
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        queryset = ParsedData.objects.filter(pk=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'output': serializer.data})

    @swagger_auto_schema(operation_summary='get list of parsed products',
                         responses={200: 'OK', 500: 'Server error'})
    def list(self, request, *args, **kwargs):
        queryset = ParsedData.objects.all()[:task_manager.product_amount]
        serializer = self.get_serializer(queryset, many=True)
        return Response({'output': serializer.data})


