from django.urls import path
from apps.home.views import Home

app_name = 'home'

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("test", Home.as_view(), name="test")
]