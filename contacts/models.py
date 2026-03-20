from django.conf import settings
from django.db import models


class EmergencyContact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    relationship = models.CharField(max_length=50, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.user.email}'


class EmergencyNotification(models.Model):
    emergency = models.ForeignKey(
        'emergencies.Emergency',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    contact = models.ForeignKey(
        EmergencyContact,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    status = models.CharField(max_length=30, default='sent_fake')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notificação {self.id} - {self.contact.name}'