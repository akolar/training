from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'presentation/index.html'
    title = 'Training :: Home'
