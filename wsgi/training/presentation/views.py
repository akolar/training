from django.shortcuts import render, redirect


def index(request):
    """Renders the index page."""

    if request.user.is_authenticated():
        return redirect('activities:overview')

    return render(request, 'presentation/index.html')
