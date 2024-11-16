from rest_framework.response import Response
from Permisos_.permisos.models import Permiso
from Permisos_.permisos.API.serializers import PermisoSerializer
from rest_framework import viewsets, status
from Utils.ResposeData import ResponseData
from rest_framework.decorators import action

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer

# Cambiar nombre de un beneficio
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

        if len(nuevo_nombre.strip()) < 4:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El nuevo nombre debe tener al menos 4 caracteres y no debe contener solo espacios.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)
        permiso = Permiso.objects.filter(nombre_permiso=nombre_actual, is_active=True).first()
        if not permiso:
            data_response= ResponseData(
                Success=False,
                Status= status.HTTP_404_NOT_FOUND,
                Message= "No hay un permiso con ese nombre",
                Record= None
            )
            return Response(data_response.toResponse(), status=status.HTTP_404_NOT_FOUND)

        permiso.nombre_permiso = nuevo_nombre
        permiso.save()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Nombre actualizado con éxito",
            Record={
                "id": permiso.id_permisos,
                "nombre_permiso": permiso.nombre_permiso
            }
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # Sobreescribir metodo CREATE
    def create(self, request, *args, **kwargs):
        nombre_permiso = request.data.get('nombre_permiso')

        # Verificar si ya existe
        if Permiso.objects.filter(nombre_permiso=nombre_permiso).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un permiso con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Permiso creado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir metodo lisT
    def list(self, request, *args, **kwargs):
        nombre_permiso = request.data.get('nombre_permiso') or request.GET.get('nombre_permiso')

        if nombre_permiso:
            queryset = Permiso.objects.filter(nombre_permiso=nombre_permiso, is_active= True)
            if not queryset.exists():
                data_response = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message=f"No hay permiso con este nombre: {nombre_permiso}",
                    Record= None
                )
                return Response(data_response.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                message="Coincidencia encontrada"
        else:
            queryset = Permiso.objects.filter(is_active=True)
            message="Lista completa de permisos"

        serializer = self.get_serializer(queryset, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # Actualizar por nombre de beneficio
    @action(detail=False, methods=['patch'], url_path='actualizar-nombre')
    def actualizar_por_nombre(self, request):
        nombre_permiso = request.data.get('nombre_permiso')
        permiso = Permiso.objects.filter(nombre_permiso=nombre_permiso, is_active=True).first()

        if not permiso:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Permiso no encontrado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = PermisoSerializer(permiso, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Permiso actualizado con éxito",
                Record=serializer.data
            )
            return Response(data.toResponse(), status=status.HTTP_200_OK)
        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=serializer.errors,
                Record=None
        )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

    # Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_permiso = request.data.get('nombre_permiso')

        if not nombre_permiso:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre de permiso no proporcionado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)


        permiso = Permiso.objects.filter(nombre_permiso=nombre_permiso, is_active=True).first()
        if not permiso:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="No hay un permiso con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        permiso.is_active = False
        permiso.save()

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Permiso eliminado con éxito.",
            Record={
                "id": permiso.id_permisos,
                "nombre_beneficio": permiso.nombre_permiso,
                "is_active": permiso.is_active
            }
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)
