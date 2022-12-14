from django.shortcuts import render
from django.views.generic import View

class Error403(View):
    def get(self, request):
        return render(request, 'guard/errores/index.html',context={'estado':403},status=403)