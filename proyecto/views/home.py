from django.shortcuts import render
from django.views.generic import View
from proyecto.auth import RoyalGuard


class Home(RoyalGuard,View):
    def get(self, request):
        context = {
        }
        return render(request, 'home/index.html', context)