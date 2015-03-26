from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def index(request):
    if request.user.is_authenticated():
        return redirect('activities:overview')

    return render(request, 'presentation/index.html')
