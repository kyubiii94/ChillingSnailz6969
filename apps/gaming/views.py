from django.shortcuts import render


def invaders(request):
    return render(request, "gaming/invaders.html")
