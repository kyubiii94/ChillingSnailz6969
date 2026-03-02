from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views import MintTransactionViewSet, SnailzViewSet

router = DefaultRouter()
router.register("snailz", SnailzViewSet, basename="snailz")
router.register("mint", MintTransactionViewSet, basename="mint")

urlpatterns = router.urls
