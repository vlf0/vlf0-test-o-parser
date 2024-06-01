from .serializers import CountSerializer
from .tasks import parse


class TasksManager:

    def __init__(self, request=None) -> None:
        self.request = request
        self.product_amount = None

    def parser_task(self) -> bool:
        if self.request is not None:
            serializer = CountSerializer(data=self.request.data)
            if serializer.is_valid():
                product_amount = serializer.data['count']
                self.product_amount = product_amount
                parse.delay(product_amount)
                return True
        return False
