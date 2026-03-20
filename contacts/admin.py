from django.contrib import admin
from .models import EmergencyContact, EmergencyNotification


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'relationship', 'is_primary', 'user', 'created_at')
    list_filter = ('is_primary',)
    search_fields = ('name', 'phone', 'email')


@admin.register(EmergencyNotification)
class EmergencyNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'emergency', 'contact', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('contact__name', 'contact__phone', 'contact__email')