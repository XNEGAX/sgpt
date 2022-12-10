from django.urls import path
from apps.guard.views.errores import PrivacyDeniedView
from apps.guard.views.usuarios import Salir

app_name = 'guard'

urlpatterns = [
    path('403/', PrivacyDeniedView.as_view(), name="403"),
    path("salir", Salir.as_view(), name="salir")
]