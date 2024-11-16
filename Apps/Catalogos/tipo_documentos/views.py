from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from Apps.Catalogos.tipo_documentos.models import Tipo_documento
from Apps.Catalogos.tipo_documentos.API.serializers import Tipo_DocumentoSerializer

class Tipo_DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_documento.objects.all()
    serializer_class = Tipo_DocumentoSerializer
