from django.contrib import admin
from django.urls import path, include
from parser_logic import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parser_logic.urls')),
]
