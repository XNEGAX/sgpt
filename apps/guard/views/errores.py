from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.response import TemplateResponse

class TemplateResponseForbidden(TemplateResponse):
    status_code = 403

class TemplateResponseNotFound(TemplateResponse):
    status_code = 404

class PrivacyDeniedView(TemplateView):
    response_class = TemplateResponseForbidden
    template_name = 'guard/errores/403.html'

class NotFoundView(TemplateView):
    response_class = TemplateResponseNotFound
    template_name = 'guard/errores/404.html'