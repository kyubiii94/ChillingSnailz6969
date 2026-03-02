from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework import permissions, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin

from .models import MintTransaction, Snailz
from .serializers import MintTransactionSerializer, SnailzSerializer


class SnailzViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Snailz.objects.select_related("faction").all()
    serializer_class = SnailzSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(ratelimit(key="user_or_ip", rate="10/m", method="POST"), name="create")
class MintTransactionViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MintTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MintTransaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
