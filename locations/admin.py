from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'point_type', 'address', 'phone', 'is_active', 'created_at')
    list_filter = ('point_type', 'is_active')
    search_fields = ('name', 'address', 'phone')