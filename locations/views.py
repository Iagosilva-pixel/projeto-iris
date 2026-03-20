from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Location
from .serializers import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(is_active=True).order_by('name')
    serializer_class = LocationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'message': 'Pontos de apoio listados com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        location = self.get_object()
        serializer = self.get_serializer(location)

        return Response({
            'success': True,
            'message': 'Ponto de apoio encontrado com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        if lat is None or lng is None:
            return Response({
                'success': False,
                'message': 'Os parâmetros lat e lng são obrigatórios.',
                'errors': {
                    'lat': ['Este parâmetro é obrigatório.'] if lat is None else [],
                    'lng': ['Este parâmetro é obrigatório.'] if lng is None else [],
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        locations = self.get_queryset()
        serializer = self.get_serializer(locations, many=True)

        return Response({
            'success': True,
            'message': 'Pontos de apoio próximos listados com sucesso.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)