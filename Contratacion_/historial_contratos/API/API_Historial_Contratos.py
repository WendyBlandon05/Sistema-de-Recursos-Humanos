from rest_framework import viewsets
from Contratacion_.historial_contratos.models import Historial_Contratos
from Contratacion_.historial_contratos.API.serializers import Historial_ContratosSerializer


class Historial_ContratosViewSet(viewsets.ModelViewSet):
    queryset = Historial_Contratos.objects.all()
    serializer_class = Historial_ContratosSerializer