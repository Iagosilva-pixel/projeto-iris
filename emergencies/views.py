from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Emergency
from .serializers import EmergencySerializer, EmergencyAudioSerializer
from contacts.models import EmergencyContact
# Importando o novo nome da função que definimos no services.py
from contacts.services import send_real_alerts


class EmergencyViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencySerializer

    def get_queryset(self):
        return Emergency.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'], url_path='activate')
    def activate(self, request):
        description = request.data.get('description', 'Botão SOS acionado')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if latitude is None or longitude is None:
            return Response({
                'success': False,
                'message': 'Latitude e longitude são obrigatórias.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Criação da Emergência (o campo address será preenchido pelo service)
        emergency = Emergency.objects.create(
            user=request.user,
            description=description,
            status='active',
            latitude=latitude,
            longitude=longitude,
        )

        contacts = EmergencyContact.objects.filter(user=request.user)

        # Chama a função que usa geopy e pywhatkit
        contacts_data = send_real_alerts(request.user, emergency, contacts)

        # Recarrega a emergency para pegar o address salvo pelo service
        emergency.refresh_from_db()
        serializer = self.get_serializer(emergency)

        return Response({
            'success': True,
            'message': 'Alerta SOS ativado com sucesso.',
            'data': {
                'emergency': serializer.data,
                'contacts_notified': contacts_data
            }
        }, status=status.HTTP_201_CREATED)

    # Mantenha os outros métodos (upload_audio, finish, etc) se desejar