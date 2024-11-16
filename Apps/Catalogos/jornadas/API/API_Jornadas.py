from Apps.Catalogos.jornadas.models import Jornada
from Apps.Catalogos.jornadas.API.serializers import JornadaSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Utils.PermisionAPI import CustomPermission
from Utils.ResposeData import ResponseData

class JornadaViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomPermission]
    queryset = Jornada.objects.all()
    serializer_class = JornadaSerializer

    # Cambiar nombre
    @action(detail=False, methods=['patch'], url_path='cambiar-nombre')
    def cambiar_nombre(self, request):
        nombre_actual = request.data.get('nombre_actual')
        nuevo_nombre = request.data.get('nuevo_nombre')

        if not nombre_actual or not nuevo_nombre:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Nombre actual o nuevo no proporcionado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if len(nuevo_nombre.strip()) < 4:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El nuevo nombre debe tener al menos 4 caracteres y no debe contener solo espacios.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if Jornada.objects.filter(nombre_jornada=nuevo_nombre, is_active=True).exclude(
                nombre_jornada=nombre_actual).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f"Ya existe una jornada con el nombre{nuevo_nombre}",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        jornada = Jornada.objects.filter(nombre_jornada=nombre_actual, is_active=True).first()
        if not jornada:
            data_response = ResponseData(
                Success= False,
                Status= status.HTTP_404_NOT_FOUND,
                Message="No hay una jornada con ese nombre",
                Record= None
            )
            return Response(data_response.toResponse(), status= status.HTTP_404_NOT_FOUND)

        jornada.nombre_jornada = nuevo_nombre
        jornada.save()
        serializer = self.get_serializer(jornada)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Nombre actualizado con éxito',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Sobreescribir método create
    def create(self, request, *args, **kwargs):
        jornada = request.data.get('nombre_jornada')

        # Verificar si ya existe
        if Jornada.objects.filter(nombre_jornada=jornada).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Ya existe una jornada con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='Jornada creada con éxito',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir list
    def list(self, request, *args, **kwargs):
        nombre_jornada = request.data.get('nombre_jornada') or request.GET.get('nombre_jornada')

        if nombre_jornada:
            queryset = Jornada.objects.filter(nombre_jornada=nombre_jornada, is_active=True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message= f"No hay una jornada con el nombre: {nombre_jornada}",
                    Record= None
                )
                return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                message =f"Coincidencia encontrada con el nombre: {nombre_jornada}"
        else:
            queryset = Jornada.objects.filter(is_active=True)
            message = "Lista completa de jornadas"

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
        nombre_jornada = request.data.get('nombre_jornada')

        if not nombre_jornada:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre de jornada no proporcionada",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        jornada = Jornada.objects.filter(nombre_jornada=nombre_jornada, is_active=True).first()

        if not jornada:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='No hay una jornada activa con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        jornada.is_active = False
        jornada.save()
        seriaalizer = self.get_serializer(jornada)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Jornada eliminada correctamente',
            Record= seriaalizer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Actualizar por nombre de la jornada
    @action(detail=False, methods=['put'], url_path='actualizar-jornada')
    def actualizar_por_nombre(self, request):
        nombre_jornada = request.data.get('nombre_jornada')

        if not nombre_jornada:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre de jornada no proporcionada",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        jornada = Jornada.objects.filter(nombre_jornada=nombre_jornada, is_active=True).first()

        if not jornada:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message=f'No existe una jornada con el nombre: {nombre_jornada}',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = JornadaSerializer(jornada, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Jornada actualizada con éxito',
                Record=serializer.data
            )
            return Response(response_data.toResponse(), status=status.HTTP_200_OK)

        response_data = ResponseData(
            Success=False,
            Status=status.HTTP_400_BAD_REQUEST,
            Message='Error en la validación',
            Record=serializer.errors
        )
        return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)