from Utils.ResposeData import ResponseData
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from Apps.Catalogos.empleados.models import Empleado
from Apps.Catalogos.empleados.API.serializers import EmpleadoSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    # Sobreescribir el metodo create
    def create(self, request, *args, **kwargs):
        numero_cedula = request.data.get('numero_cedula')

        # Verificar si ya existe ese numero de cédula
        if Empleado.objects.filter(numero_cedula=numero_cedula, is_active=True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Ya existe un empleado registrado con este número de cédula.',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        #Serializar datos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='Empleado creado con éxito.',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir list
    def list(self, request, *args, **kwargs):
        numero_cedula = request.data.get('numero_cedula') or request.GET.get('numero_cedula')

        if numero_cedula:
            queryset = Empleado.objects.filter(numero_cedula=numero_cedula, is_active= True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message=f"No hay un empleado asociado a esta cédula de identidad: {numero_cedula}",
                    Record=None
                )
                return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)
            else:
                message = f"Empleado encontrado con: {numero_cedula}"
        else:
            queryset = Empleado.objects.filter(is_active= True)
            message = "Lista de empleados activos"

        serializer = self.get_serializer(queryset, many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # Eliminar por número de cédula
    @action(detail=False, methods=['delete'], url_path='eliminar-cedula')
    def eliminar_cedula(self, request):
        numero_cedula = request.data.get('numero_cedula')
        if not numero_cedula:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Digite el número de cédula.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        empleado = Empleado.objects.filter(numero_cedula=numero_cedula, is_active=True).first()

        if not empleado:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f'No hay un empleado asociado a este número de cédula: {numero_cedula}',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        empleado.is_active = False
        empleado.save()
        serializer = self.get_serializer(empleado)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Empleado eliminado con éxito.',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)


    # Actualizar por número de cédula
    @action(detail=False, methods=['put'], url_path='actualizar-empleado-cedula')
    def actualizar_empleado_cedula(self, request):
        numero_cedula = request.data.get('numero_cedula')

        if not numero_cedula:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Digite el número de cédula.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        empleado = Empleado.objects.filter(numero_cedula=numero_cedula, is_active=True).first()
        if not empleado:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='Empleado no encontrado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = EmpleadoSerializer(empleado, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Empleado actualizado con éxito',
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

    # CAMBIAR NUMERO DE CEDULA
    @action(detail=False, methods=['patch'], url_path='actualizar-cedula')
    def actualizar_cedula(self, request):
        cedula_actual = request.data.get('cedula_actual')
        nueva_cedula = request.data.get('nueva_cedula')

        if not cedula_actual or not nueva_cedula:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Falta un valor, cédula registrada, o la nueva versión de la cédula",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if Empleado.objects.filter(numero_cedula=nueva_cedula, is_active=True).exclude(
                numero_cedula=cedula_actual).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f"El número de cédula: {nueva_cedula} esta asociada a otro empleado, verifique nuevamente",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        empleado = Empleado.objects.filter(numero_cedula=cedula_actual, is_active=True).first()
        if not empleado:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message=f"No hay un empleado con este número de cédula: {cedula_actual}",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        empleado.numero_cedula = nueva_cedula
        empleado.save()
        serializer = self.get_serializer(empleado)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Número de cédula actualizado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)
