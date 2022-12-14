from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import View
from django.views.generic import ListView
from apps.guard.auth import RoyalGuard
# models
from apps.guard.models import User

class MantenedorUsuario(RoyalGuard,ListView):
    template_name = 'guard/usuarios/mantenedor.html'
    paginate_by = 10
    model = User

    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        new_context = User.objects.filter(
            Q(first_name__icontains=filter_val)|Q(last_name__icontains=filter_val)|Q(username__icontains=filter_val),
            email__icontains='edu.udla.cl',id__gte=1,
        ).order_by('username')
        return new_context

    def get_context_data(self, **kwargs):
        context = super(MantenedorUsuario, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
        return context