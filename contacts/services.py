from .models import EmergencyNotification


def send_fake_alerts(user, emergency, contacts):
    notified_contacts = []

    message = (
        f"ALERTA SOS\n"
        f"Usuária: {user.email}\n"
        f"Emergência ID: {emergency.id}\n"
        f"Descrição: {emergency.description}\n"
        f"Localização: ({emergency.latitude}, {emergency.longitude})\n"
    )

    for contact in contacts:
        notification = EmergencyNotification.objects.create(
            emergency=emergency,
            contact=contact,
            message=message,
            status='sent_fake'
        )

        notified_contacts.append({
            'id': notification.id,
            'name': contact.name,
            'phone': contact.phone,
            'email': contact.email,
            'relationship': contact.relationship,
            'message': message,
            'status': notification.status,
            'created_at': notification.created_at,
        })

    return notified_contacts