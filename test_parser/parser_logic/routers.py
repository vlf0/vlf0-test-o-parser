from rest_framework import routers
from .views import ParsedDataViewSet, ParserRunnerViewSet

router = routers.DefaultRouter()

router.register(r'parsed_data', ParsedDataViewSet, basename='parsed_data')
router.register(r'run_parsing', ParserRunnerViewSet, basename='run_parsing')

