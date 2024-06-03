from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_score(self, value: int):
        if 1 <= value <= 5:
            return value
        raise serializers.ValidationError(
            {'score':  'Only integers from 1 to 5 are valid'}
        )

    def validate_restaurant(self, value):
        if self.instance:
            raise serializers.ValidationError(
                {'restaurant': 'You cannot update the restaurant of a review'},
            )
        return value
