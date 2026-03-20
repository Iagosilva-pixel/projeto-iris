from rest_framework import serializers
from .models import Emergency, EmergencyAudio


class EmergencySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Emergency
        fields = [
            'id',
            'user',
            'description',
            'status',
            'latitude',
            'longitude',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at']


class EmergencyAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAudio
        fields = ['id', 'audio_file', 'created_at']
        read_only_fields = ['id', 'created_at']