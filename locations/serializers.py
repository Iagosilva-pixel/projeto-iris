from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'point_type',
            'address',
            'latitude',
            'longitude',
            'phone',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']