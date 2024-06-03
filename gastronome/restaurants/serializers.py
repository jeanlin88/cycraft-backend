from django.db.models import Avg, QuerySet
from rest_framework import serializers

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        ordering = ['-created_at']

    def get_rating(self, obj: Restaurant):
        reviews: QuerySet = obj.review_set
        if reviews.exists():
            return reviews.aggregate(Avg("score"))['score__avg']
        return None

    def get_total_reviews(self, obj: Restaurant):
        return obj.review_set.count()
