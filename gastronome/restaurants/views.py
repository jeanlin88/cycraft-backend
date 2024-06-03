from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from users.permissions import ModifyAndIsBusiness, NotCreateAndIsObjectOwner

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.annotate(
        rating=Avg('review__score'),
        total_reviews=Count('review'),
    ).order_by('created_at')
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['rating']
    permission_classes = (
        permissions.IsAuthenticated,
        ModifyAndIsBusiness,
        NotCreateAndIsObjectOwner,
    )

    def create(self, request: Request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = str(self.request.user.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
