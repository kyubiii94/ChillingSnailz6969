from django.urls import path

from . import views

app_name = "gaming"

urlpatterns = [
    path("invaders/", views.invaders, name="invaders"),
]
