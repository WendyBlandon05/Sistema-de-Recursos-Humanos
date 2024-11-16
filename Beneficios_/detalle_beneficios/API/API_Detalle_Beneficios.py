from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Contratacion_.contratos.models import Contrato
from Beneficios_.detalle_beneficios.API.serializers import Detalle_BeneficioSerializer
from Beneficios_.detalle_beneficios.models import Detalle_Beneficios
from Utils.ResposeData import ResponseData

class Detalle_BeneficioViewSet(viewsets.ModelViewSet):
    queryset = Detalle_Beneficios.objects.all()
    serializer_class = Detalle_BeneficioSerializer

    # metodo create
    def create(self, request, *args, **kwargs):
        id_contrato = request.data.get('id_contrato')
        id_beneficios = request.data.get('id_beneficios')

        if Detalle_Beneficios.objects.filter(id_contrato=id_contrato, id_beneficios=id_beneficios, is_active=True).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El beneficio que intenta asociar ya esta enlazado a este contrato",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Detalle de beneficio creado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_201_CREATED)

    #METODO LIST POR CONTRATO
    def list(self, request, *args, **kwargs):
        codigo_contrato = request.data.get('codigo')

        if codigo_contrato:
            contratos = Contrato.objects.filter(codigo_contrato=codigo_contrato, is_active=True)

            if contratos.exists():
                queryset = Detalle_Beneficios.objects.filter(id_contrato__in=contratos, is_active=True)
                if not queryset.exists():
                    return Response({
                        "Success": True,
                        "Status": status.HTTP_204_NO_CONTENT,
                        "Message": f"El contrato con código {codigo_contrato} no tiene beneficios asociados",
                        "Record": None
                    }, status=status.HTTP_200_OK)
                message = f"Detalles de beneficios asociados al contrato con código {codigo_contrato}"
            else:
                return Response({
                    "Success": False,
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "Contrato no encontrado",
                    "Record": None
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Detalle_Beneficios.objects.filter(is_active=True)
            message = "Lista completa de detalles de beneficios activos"

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "Success": True,
            "Status": status.HTTP_200_OK,
            "Message": message,
            "Record": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


# Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-detalle-beneficio')
    def eliminar_detalle(self, request):
        id_beneficios = request.data.get('id_detalle_beneficios')

        if not id_beneficios:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="ID no proporcionado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        det_beneficio = Detalle_Beneficios.objects.filter(id_detalle_beneficios=id_beneficios, is_active=True).first()

        if not det_beneficio:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f'No hay un detalle de beneficio activo con el ID: {id_beneficios}',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        det_beneficio.is_active = False
        det_beneficio.save()
        serializer = self.get_serializer(det_beneficio)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Detalle de beneficio eliminado con éxito.',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    #Modificar
    @action(detail=False, methods=['put'], url_path='modificar-detalle')
    def modificar_detalle(self, request):
        id_detalle = request.data.get('id_detalle_beneficios')
        if not id_detalle:
            data_response =ResponseData(
                Success= False,
                Status= status.HTTP_400_BAD_REQUEST,
                Message= "Proporcione el ID del detalle que desea modificar",
                Record= None
            )
            return Response(data_response.toResponse(), status= status.HTTP_400_BAD_REQUEST)
        detalle = Detalle_Beneficios.objects.filter(id_detalle_beneficios = id_detalle, is_active = True).first()

        if not detalle:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message=f"No hay un detalle de beneficio con el ID: {id_detalle}",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = Detalle_BeneficioSerializer(detalle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Detalle de Beneficio actualizado con éxito",
                Record=serializer.data
            )
            return Response(data.toResponse(), status=status.HTTP_200_OK)

        data = ResponseData(
            Success=False,
            Status=status.HTTP_400_BAD_REQUEST,
            Message="Errores en los datos, verifique",
            Record=None
        )
        return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)