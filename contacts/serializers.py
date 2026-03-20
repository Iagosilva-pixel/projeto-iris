from rest_framework import serializers
from .models import EmergencyContact


class EmergencyContactSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EmergencyContact
        fields = [
            'id',
            'user',
            'name',
            'phone',
            'email',
            'relationship',
            'is_primary',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']