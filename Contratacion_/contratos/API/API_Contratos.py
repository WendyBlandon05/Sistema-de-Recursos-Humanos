from rest_framework.decorators import action
from rest_framework.response import Response
from Utils.ResposeData import ResponseData
from Contratacion_.contratos.API.serializers import ContratoSerializer
from Contratacion_.contratos.models import Contrato
from rest_framework import viewsets, status

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

 # Cambiar código de contrato
    @action(detail=False, methods=['patch'], url_path='cambiar-codigo')
    def cambiar_codigo(self, request):
        codigo_actual = request.data.get('codigo_actual')
        nuevo_codigo = request.data.get('nuevo_codigo')

        if not codigo_actual or not nuevo_codigo:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Código actual o nuevo no proporcionado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if len(nuevo_codigo) != 8 or ' ' in nuevo_codigo:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El código del contrato debe tener exactamente 8 caracteres y no contener espacios en blanco",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if Contrato.objects.filter(codigo_contrato=nuevo_codigo, is_active=True).exclude(
                codigo_contrato=codigo_actual).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un contrato con ese código digite uno diferente",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)


        contrato = Contrato.objects.filter(codigo_contrato=codigo_actual, is_active=True).first()
        if not contrato:
            response_data = ResponseData(
                Success= False,
                Status= status.HTTP_404_NOT_FOUND,
                Message="No existe contrato con ese código",
                Record= None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        contrato.codigo_contrato = nuevo_codigo
        contrato.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Código de contrato actualizado con éxito',
            Record={
                "id_contrato":contrato.id_contratos,
                "codigo_contrato":contrato.codigo_contrato
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    #Sobreescribir create
    def create(self, request, *args, **kwargs):
        codigo = request.data.get('codigo_contrato')

        # Verificar si ya existe
        if Contrato.objects.filter(codigo_contrato=codigo, is_active= True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Ya existe un contrato con ese código',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='Contrato creado con éxito',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir list
    def list(self, request, *args, **kwargs):
        codigo = request.data.get('codigo_contrato') or request.GET.get('codigo_contrato')

        if codigo:
            queryset = Contrato.objects.filter(codigo_contrato=codigo, is_active=True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message= "No hay un contrato con ese código",
                    Record= None
                )
                return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                message= f"Coincidencia encontrada con: {codigo}"
        else:
            queryset = Contrato.objects.filter(is_active=True)
            message = "Listas de Contratos activos"

        serializer = self.get_serializer(queryset, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # Eliminar por código de contrato
    @action(detail=False, methods=['delete'], url_path='eliminar-codigo')
    def eliminar_codigo(self, request):
        codigo = request.data.get('codigo_contrato')

        contrato = Contrato.objects.filter(codigo_contrato=codigo, is_active=True).first()

        if not contrato:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='No hay un contrato con ese código',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        contrato.is_active = False
        contrato.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Contrato eliminado con éxito.',
            Record={
                "id": contrato.id_contratos,
                "codigo_contrato": contrato.codigo_contrato,
                "is_active": contrato.is_active
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Actualizar por código de contrato
    @action(detail=False, methods=['put'], url_path='actualizar-contrato')
    def actualizar_por_codigo(self, request):
        codigo = request.data.get('codigo_contrato')
        contrato = Contrato.objects.filter(codigo_contrato=codigo, is_active = True).first()

        if not contrato:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='Contrato no encontrado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = ContratoSerializer(contrato, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Contrato actualizado con éxito',
                Record=serializer.data
            )
            return Response(response_data.toResponse(), status=status.HTTP_200_OK)

        response_data = ResponseData(
            Success=False,
            Status=status.HTTP_400_BAD_REQUEST,
            Message='Error en los datos insertados, verifique',
            Record=serializer.errors
        )
        return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)