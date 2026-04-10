import pywhatkit as kit
from geopy.geocoders import Nominatim
from .models import EmergencyNotification
import logging


def get_address_from_coords(lat, lon):
    """Consulta o Nominatim (OSM) para obter o endereço amigável."""
    try:
        # User_agent é obrigatório pelo OSM
        geolocator = Nominatim(user_agent="projeto_iris_sos")
        location = geolocator.reverse(f"{lat}, {lon}", timeout=10)
        return location.address if location else "Endereço não identificado"
    except Exception as e:
        logging.error(f"Erro ao buscar endereço: {e}")
        return "Localização aproximada (ver link do mapa)"


def send_real_alerts(user, emergency, contacts):
    """Descobre o endereço e envia via WhatsApp real."""
    # 1. Descobrir o nome da rua/bairro
    readable_address = get_address_from_coords(emergency.latitude, emergency.longitude)

    # Salva o endereço no banco de dados
    emergency.address = readable_address
    emergency.save()

    # 2. Gerar o link do Google Maps
    google_maps_url = f"https://www.google.com/maps?q={emergency.latitude},{emergency.longitude}"

    message_body = (
        f"🚨 *ALERTA SOS - PROJETO ÍRIS* 🚨\n\n"
        f"A usuária *{user.email}* precisa de ajuda!\n\n"
        f"📍 *ENDEREÇO:* {readable_address}\n"
        f"🔗 *MAPA:* {google_maps_url}\n"
        f"📝 *NOTA:* {emergency.description}"
    )

    notified_contacts = []

    # 3. Envio via pywhatkit
    for contact in contacts:
        try:
            # Abre o WhatsApp Web e envia a mensagem
            kit.sendwhatmsg_instantly(
                phone_no=contact.phone,
                message=message_body,
                wait_time=15,
                tab_close=True
            )
            status = 'sent'
        except Exception as e:
            logging.error(f"Erro ao enviar para {contact.name}: {e}")
            status = 'failed'

        # Registra a notificação no banco de dados
        EmergencyNotification.objects.create(
            emergency=emergency,
            contact=contact,
            message=message_body,
            status=status
        )
        notified_contacts.append({'name': contact.name, 'status': status})

    return notified_contacts