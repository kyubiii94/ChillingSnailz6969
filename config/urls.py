from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("collection/", include("apps.nft.urls")),
    path("gaming/", include("apps.gaming.urls")),
    path("api/v1/", include("apps.nft.api_urls")),
    path("", include("apps.core.urls")),
]
