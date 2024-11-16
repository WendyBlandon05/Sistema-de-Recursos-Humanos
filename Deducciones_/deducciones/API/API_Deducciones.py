from rest_framework.decorators import action
from rest_framework.response import Response
from Utils.ResposeData import ResponseData
from Deducciones_.deducciones.models import Deducciones
from Deducciones_.deducciones.API.serializers import DeduccionesSerializer
from rest_framework import viewsets, status

class DeduccionesViewSet(viewsets.ModelViewSet):
    queryset = Deducciones.objects.all()
    serializer_class = DeduccionesSerializer

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

        if Deducciones.objects.filter(nombre_deduccion=nuevo_nombre, is_active=True).exclude(
                nombre_deduccion=nombre_actual).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f"Ya existe una deduccion con el nombre:{nuevo_nombre}",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        deduccion = Deducciones.objects.filter(nombre_deduccion=nombre_actual, is_active= True).first()
        if not deduccion:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message=f"No hay una deducción con el nombre {nombre_actual}",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        deduccion.nombre_deduccion = nuevo_nombre
        deduccion.save()

        serializer = self.get_serializer(deduccion)
        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Nombre de deducción actualizado con éxito',
            Record= serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)


    # Sobreescribir metodo create
    def create(self, request, *args, **kwargs):
        nombre_deduccion = request.data.get('nombre_deduccion')

        if Deducciones.objects.filter(nombre_deduccion=nombre_deduccion, is_active= True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Ya existe una deducción con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='Deducción creada con éxito',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)


    # Sobreescribir list
    def list(self, request, *args, **kwargs):
        nombre_deduccion = request.data.get('nombre_deduccion') or request.GET.get('nombre_deduccion')

        if nombre_deduccion:
            queryset = Deducciones.objects.filter(nombre_deduccion=nombre_deduccion, is_active=True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message= "No hay una deducción con ese nombre",
                    Record= None
                )
                return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                message = f"Coincidencia con el nombre: {nombre_deduccion}"
        else:
            queryset = Deducciones.objects.filter(is_active=True)
            message = "Lista completa de deducciones"

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
        nombre_deduccion = request.data.get('nombre_deduccion')

        if not nombre_deduccion:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre de la deducción no proporcionado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        deduccion = Deducciones.objects.filter(nombre_deduccion=nombre_deduccion, is_active=True).first()

        if not deduccion:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='No hay una deducción activa con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        deduccion.is_active = False
        deduccion.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Deducción eliminada con éxito.',
            Record={
                "id_deducciones": deduccion.id_deducciones,
                "nombre_deduccion": deduccion.nombre_deduccion,
                "is_active": deduccion.is_active
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)


    # Actualizar por nombre de deducción
    @action(detail=False, methods=['put'], url_path='actualizar-deduccion')
    def actualizar_por_nombre(self, request):
        nombre_deduccion = request.data.get('nombre_deduccion')

        deduccion = Deducciones.objects.filter(nombre_deduccion=nombre_deduccion, is_active=True).first()
        if not deduccion:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='Deducción no encontrada',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = DeduccionesSerializer(deduccion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Deducción actualizada con éxito',
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