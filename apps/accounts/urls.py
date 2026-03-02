from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("export-data/", views.export_data, name="export-data"),
    path("delete-account/", views.delete_account, name="delete-account"),
]
