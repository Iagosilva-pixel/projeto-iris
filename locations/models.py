from django.db import models


class Location(models.Model):
    TYPE_CHOICES = [
        ('police', 'Delegacia'),
        ('psychological', 'Apoio Psicológico'),
        ('shelter', 'Abrigo'),
        ('hospital', 'Hospital'),
        ('legal', 'Apoio Jurídico'),
    ]

    name = models.CharField(max_length=255)
    point_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name