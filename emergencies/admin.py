from django.contrib import admin
from .models import Emergency, EmergencyAudio


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'latitude', 'longitude', 'created_at')
    list_filter = ('status',)


@admin.register(EmergencyAudio)
class EmergencyAudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'emergency', 'audio_file', 'created_at')