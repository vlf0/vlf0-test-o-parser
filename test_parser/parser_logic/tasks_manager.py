from .serializers import CountSerializer
from .tasks import parse


class TasksManager:
    """
    A class for managing tasks related to parsing products after receiving a request from an API view.

    Attributes:
      request: The HTTP request object containing request data.
      product_amount: The number of products to parse.
    """

    def __init__(self, request=None) -> None:
        """
        Initialize an instance of TasksManager.

        :param request: The HTTP request object containing request data (default is None).
        """
        self.request = request
        self.product_amount = None

    def parser_task(self) -> bool:
        """
        Validates the request data and initiates a parsing task.

        :return: True if the parsing task was successfully initiated, False otherwise.
        """
        if self.request is not None:
            serializer = CountSerializer(data=self.request.data)
            if serializer.is_valid():
                product_amount = serializer.data['count']
                self.product_amount = product_amount
                parse.delay(product_amount)
                return True
        return False
