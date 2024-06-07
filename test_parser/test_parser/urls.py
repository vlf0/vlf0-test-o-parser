from django.contrib import admin
from django.urls import path, include
from parser_logic import urls
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parser_logic.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]

