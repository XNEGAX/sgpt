from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from apps.guard.auth import RoyalGuard
from django.contrib.auth.views import LogoutView

class Salir(LogoutView):
    def get(self, request, *args, **kwargs):
        rediredct_login = f'/admin/login/?next=/'
        print(rediredct_login)
        return redirect(rediredct_login)