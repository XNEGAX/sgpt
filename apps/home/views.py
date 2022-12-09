from django.shortcuts import render
from django.views.generic import View
from apps.guard.auth import RoyalGuard


class Home(RoyalGuard,View):
    def get(self, request):
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
        context = {
        }
        return render(request, 'home/index.html', context)