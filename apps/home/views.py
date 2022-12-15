from django.shortcuts import render
from django.views.generic import View
from apps.guard.auth import RoyalGuard


class Home(RoyalGuard,View):
    def get(self, request):
        import requests
        url = 'https://miudla.udla.cl/'
        response = requests.get(url)
        print(response.text)
        context = {
        }
        return render(request, 'home/index.html', context)