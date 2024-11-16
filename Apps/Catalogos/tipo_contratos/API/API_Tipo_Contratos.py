from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Utils.ResposeData import ResponseData
from Apps.Catalogos.tipo_contratos.models import Tipo_contrato
from Apps.Catalogos.tipo_contratos.API.serializers import Tipo_ContratoSerializer

class Tipo_ContratoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_contrato.objects.all()
    serializer_class = Tipo_ContratoSerializer

    # Cambiar nombre
    @action(detail=False, methods=['patch'], url_path='cambiar-nombre')
    def cambiar_nombre(self, request):
        nombre_actual = request.data.get('nombre_actual')
        nuevo_nombre = request.data.get('nuevo_nombre')

        if not nombre_actual or not nuevo_nombre:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre actual o nuevo no proporcionado",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if len(nuevo_nombre.strip()) < 3:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El nuevo nombre debe tener al menos 3 caracteres y no debe contener solo espacios.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        contrato = Tipo_contrato.objects.filter(nombre_tipo=nombre_actual, is_active=True).first()

        if not contrato:
            response_data=ResponseData(
                Success= False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="No hay un registro con ese nombre",
                Record= None
            )
            return Response(response_data.toResponse(),status= status.HTTP_404_NOT_FOUND)

        contrato.nombre_tipo = nuevo_nombre
        contrato.save()

        serializer = self.get_serializer(contrato)
        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Nombre actualizado con éxito",
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Sobreescribir metodo create
    def create(self, request, *args, **kwargs):
        nombre_tipo = request.data.get('nombre_tipo')

        if Tipo_contrato.objects.filter(nombre_tipo=nombre_tipo, is_active=True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un tipo de contrato con ese nombre",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Tipo de contrato creado",
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir metodo LIST
    def list(self, request, *args, **kwargs):
        nombre_tipo = request.data.get('nombre_tipo') or request.GET.get('nombre_tipo')

        if nombre_tipo:
            queryset = Tipo_contrato.objects.filter(nombre_tipo=nombre_tipo, is_active=True)
            if not queryset.exists():
                data_response = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message="No hay un tipo de contrato con ese nombre",
                    Record= None
                )
                return Response(data_response.toResponse(),status=status.HTTP_404_NOT_FOUND)
            else:
                message = f"Coincidencia encontrada con: {nombre_tipo}"
        else:
            queryset = Tipo_contrato.objects.filter(is_active=True)
            message = "Lista completa de tipos de contrato"

        serializer = self.get_serializer(queryset, many=True)
        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Eliminar  por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_tipo = request.data.get('nombre_tipo')

        if not nombre_tipo:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Debe proporcionar un nombre de tipo de contrato válido",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        contrato = Tipo_contrato.objects.filter(nombre_tipo=nombre_tipo, is_active=True).first()
        if not contrato:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="No hay un tipo de contrato con ese nombre",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        contrato.is_active = False
        contrato.save()

        serializer = self.get_serializer(contrato)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Tipo de contrato eliminado con éxito",
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)