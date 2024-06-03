from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from users.permissions import ModifyAndIsNotBusiness, NotCreateAndIsObjectOwner

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.order_by('created_at')
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['score']
    filterset_fields = ['restaurant', 'created_by']
    permission_classes = (
        permissions.IsAuthenticated,
        ModifyAndIsNotBusiness,
        NotCreateAndIsObjectOwner,
    )

    def list(self, request: Request, *args, **kwargs):
        restaurant_id = request.query_params.get('restaurant', None)
        created_by_id = request.query_params.get('created_by', None)

        if restaurant_id is None and created_by_id is None:
            return Response(
                {"error": "At least one of 'restaurant' or 'created_by' filters is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().list(request=request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = str(self.request.user.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
