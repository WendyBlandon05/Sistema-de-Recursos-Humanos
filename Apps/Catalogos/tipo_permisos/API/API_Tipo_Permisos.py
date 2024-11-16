from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Apps.Catalogos.tipo_permisos.models import Tipo_permiso
from Apps.Catalogos.tipo_permisos.API.serializers import TipoPermisoSerializer
from Utils.ResposeData import ResponseData

class TipoPermisoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_permiso.objects.all()
    serializer_class = TipoPermisoSerializer

# Cambiar nombre del tipo de permiso
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

        permiso = Tipo_permiso.objects.filter(nombre_tipo_permiso=nombre_actual, is_active=True).first()

        if not permiso:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="No hay un tipo de permiso con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        permiso.nombre_tipo_permiso = nuevo_nombre
        permiso.save()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Nombre actualizado con éxito",
            Record={
                "id": permiso.id_tipo_permisos,
                "nombre_tipo_permiso": permiso.nombre_tipo_permiso
            }
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # Sobreescribir metodo create
    def create(self, request, *args, **kwargs):
        nombre_tipo_permiso = request.data.get('nombre_tipo_permiso')

        if Tipo_permiso.objects.filter(nombre_tipo_permiso=nombre_tipo_permiso, is_active=True).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un tipo de permiso con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Tipo de permiso creado",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir el metodo list
    def list(self, request, *args, **kwargs):
        nombre_tipo_permiso = request.data.get('nombre_tipo_permiso') or request.GET.get('nombre_tipo_permiso')

        if nombre_tipo_permiso:
            queryset = Tipo_permiso.objects.filter(nombre_tipo_permiso=nombre_tipo_permiso, is_active=True)
            if not queryset.exists():
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message=f"No se encontró ningún tipo de permiso con el nombre: {nombre_tipo_permiso}",
                    Record=None
                )
                return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)
            else:
                message = f"Coincidencia encontrada con: {nombre_tipo_permiso}"
        else:
            queryset = Tipo_permiso.objects.filter(is_active=True)
            message = "Lista completa de tipos de permiso"

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
        nombre_tipo_permiso = request.data.get('nombre_tipo_permiso')

        if not nombre_tipo_permiso:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Debe proporcionar un nombre de tipo de permiso válido",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        permiso = Tipo_permiso.objects.filter(nombre_tipo_permiso=nombre_tipo_permiso, is_active=True).first()

        if not permiso:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="No hay un tipo de permiso con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        permiso.is_active = False
        permiso.save()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Tipo de permiso eliminado con éxito.",
            Record={
                "id": permiso.id_tipo_permisos,
                "nombre_tipo_permiso": permiso.nombre_tipo_permiso,
                "is_active": permiso.is_active
            }
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

