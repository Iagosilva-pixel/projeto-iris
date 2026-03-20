from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Emergency
from .serializers import EmergencySerializer, EmergencyAudioSerializer
from contacts.models import EmergencyContact
from contacts.services import send_fake_alerts


class EmergencyViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencySerializer

    def get_queryset(self):
        return Emergency.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'message': 'Emergências listadas com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        emergency = self.get_object()
        serializer = self.get_serializer(emergency)

        return Response({
            'success': True,
            'message': 'Emergência encontrada com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response({
            'success': True,
            'message': 'Emergência criada com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='activate')
    def activate(self, request):
        description = request.data.get('description', 'Botão SOS acionado')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if latitude is None or longitude is None:
            return Response({
                'success': False,
                'message': 'Latitude e longitude são obrigatórias.',
                'errors': {
                    'latitude': ['Este campo é obrigatório.'] if latitude is None else [],
                    'longitude': ['Este campo é obrigatório.'] if longitude is None else [],
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        existing_emergency = Emergency.objects.filter(
            user=request.user,
            status='active'
        ).first()

        if existing_emergency:
            serializer = self.get_serializer(existing_emergency)
            return Response({
                'success': False,
                'message': 'Você já possui um alerta SOS ativo.',
                'data': serializer.data
            }, status=status.HTTP_400_BAD_REQUEST)

        emergency = Emergency.objects.create(
            user=request.user,
            description=description,
            status='active',
            latitude=latitude,
            longitude=longitude,
        )

        contacts = EmergencyContact.objects.filter(user=request.user)
        contacts_data = send_fake_alerts(request.user, emergency, contacts)
        serializer = self.get_serializer(emergency)

        return Response({
            'success': True,
            'message': 'Alerta SOS ativado com sucesso.',
            'data': {
                'emergency': serializer.data,
                'contacts_notified': contacts_data,
                'total_contacts': contacts.count()
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='audio')
    def upload_audio(self, request, pk=None):
        emergency = self.get_object()

        if 'audio_file' not in request.FILES:
            return Response({
                'success': False,
                'message': 'O arquivo de áudio é obrigatório.',
                'errors': {
                    'audio_file': ['Envie um arquivo de áudio.']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmergencyAudioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(emergency=emergency)

        return Response({
            'success': True,
            'message': 'Áudio enviado com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='finish')
    def finish(self, request, pk=None):
        emergency = self.get_object()

        if emergency.status != 'active':
            return Response({
                'success': False,
                'message': 'Esta emergência já foi finalizada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        emergency.status = 'resolved'
        emergency.save()

        serializer = self.get_serializer(emergency)

        return Response({
            'success': True,
            'message': 'Emergência finalizada com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)