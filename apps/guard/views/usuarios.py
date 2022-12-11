from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

class Salir(LogoutView):
    def get(self, request, *args, **kwargs):
        rediredct_login = f'/admin/login/?next=/'
        return redirect(rediredct_login)