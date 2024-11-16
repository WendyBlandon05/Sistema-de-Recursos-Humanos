from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Apps.Catalogos.tipo_documentos.models import Tipo_documento
from Utils.ResposeData import ResponseData
from Apps.Catalogos.tipo_documentos.API.serializers import Tipo_DocumentoSerializer

class Tipo_DocumentosViewSet(viewsets.ModelViewSet):
    queryset = Tipo_documento.objects.all()
    serializer_class = Tipo_DocumentoSerializer

       #cambiar nombre
    @action(detail=False, methods=['patch'], url_path='cambiar-nombre')
    def cambiar_nombre(self, request):
        nombre_actual = request.data.get('nombre_actual')
        nuevo_nombre = request.data.get('nuevo_nombre')

        if not nombre_actual or not nuevo_nombre:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre actual o nuevo no proporcionado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if len(nuevo_nombre.strip()) < 3:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El nuevo nombre debe tener al menos 3 caracteres y no debe contener solo espacios.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        documento = Tipo_documento.objects.filter(nombre_tipo_documentos=nombre_actual, is_active=True).first()
        if not documento:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="No hay un tipo de documento con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        documento.nombre_tipo_documentos = nuevo_nombre
        documento.save()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Nombre actualizado con éxito",
            Record={
                "id": documento.id_tipo_documentos,
                "nombre_tipo_documentos": documento.nombre_tipo_documentos
            }
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)


    # Sobrescribir metodo create
    def create(self, request, *args, **kwargs):
        nombre_tipo_documentos = request.data.get('nombre_tipo_documentos')

        if Tipo_documento.objects.filter(nombre_tipo_documentos=nombre_tipo_documentos, is_active=True).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un tipo de documento con ese nombre, cambie el nombre e intente nuevamente",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Tipo de documento creado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_201_CREATED)


    # Sobrescribir metodo list
    def list(self, request, *args, **kwargs):
        nombre_tipo_documentos = request.data.get('nombre_tipo_documentos') or request.GET.get('nombre_tipo_documentos')

        if nombre_tipo_documentos:
            queryset = Tipo_documento.objects.filter(nombre_tipo_documentos=nombre_tipo_documentos, is_active=True)
            if not queryset.exists():
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message=f"No se encontró ningún tipo de documento con el nombre: {nombre_tipo_documentos}",
                    Record=None
                )
                return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)
            else:
                message = f"Coincidencia encontrada con: {nombre_tipo_documentos}"
        else:
            queryset = Tipo_documento.objects.filter(is_active=True)
            message = "Lista completa de tipos de documento"

        serializer = self.get_serializer(queryset, many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)


    # Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_tipo_documentos = request.data.get('nombre_tipo_documentos')

        if not nombre_tipo_documentos:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Debe proporcionar un nombre de tipo de documento válido",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        documento = Tipo_documento.objects.filter(nombre_tipo_documentos=nombre_tipo_documentos, is_active=True).first()

        if not documento:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="No hay un tipo de documento con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        documento.is_active = False
        documento.save()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Tipo de documento eliminado con éxito",
            Record={
                "id": documento.id_tipo_documentos,
                "nombre_tipo_documentos": documento.nombre_tipo_documentos,
                "is_active": documento.is_active
            }
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)
