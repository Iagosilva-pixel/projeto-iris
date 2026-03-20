from django.conf import settings
from django.db import models


class Emergency(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('resolved', 'Resolvido'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emergencies'
    )
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Alerta #{self.id} - {self.user.email}'


class EmergencyAudio(models.Model):
    emergency = models.ForeignKey(
        Emergency,
        on_delete=models.CASCADE,
        related_name='audios'
    )
    audio_file = models.FileField(upload_to='emergency_audios/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Áudio {self.id} - Emergência {self.emergency.id}'