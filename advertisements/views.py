from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (BasePermission, IsAdminUser,
                                        IsAuthenticated)
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.serializers import AdvertisementSerializer, UserSerializer


class AdvertisementPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return (obj.creator == request.user)
        return super().has_object_permission(request, view, obj)

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = AdvertisementFilter
    permission_classes = [AdvertisementPermissions | IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Advertisement.objects.all().exclude(
                ~Q(creator=self.request.user),
                status=AdvertisementStatusChoices.DRAFT
            )
        else:
            return Advertisement.objects.all().exclude(
                status=AdvertisementStatusChoices.DRAFT
            )

    # def get_permissions(self):
    #     """Получение прав для действий."""
    #     if self.action in ['create', 'update', 'partial_update']:
    #         return [IsAuthenticated()]
    #     return []
