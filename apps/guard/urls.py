from django.urls import path
from apps.guard.views.errores import PrivacyDeniedView

app_name = 'guard'

urlpatterns = [
    path('403/', PrivacyDeniedView.as_view(), name="403"),
    # path("logout/", LogoutView.as_view(), name="logout")
]