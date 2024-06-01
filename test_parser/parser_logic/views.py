from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import ParsingSerializer
from .models import ParsedData
from .tasks_manager import TasksManager

task_manager = TasksManager()


class ParserRunnerViewSet(viewsets.ViewSet):

    http_method_names = ['post']

    def create(self, request):
        task_manager.request = request
        if task_manager.parser_task():
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


class ParsedDataViewSet(viewsets.ModelViewSet):

    http_method_names = ['get']
    serializer_class = ParsingSerializer

    def get_queryset(self):
        queryset = ParsedData.objects.all()[:task_manager.product_amount]
        return queryset


