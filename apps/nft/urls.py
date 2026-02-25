from django.urls import path

from . import views

app_name = "nft"

urlpatterns = [
    path("", views.collection, name="collection"),
]
