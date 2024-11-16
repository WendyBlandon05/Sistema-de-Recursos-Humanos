from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Contratacion_.contratos.models import Contrato
from Deducciones_.detalle_deducciones.API.serializers import Detalle_DeduccionesSerializer
from Deducciones_.detalle_deducciones.models import Detalle_Deducciones
from Utils.ResposeData import ResponseData

class Detalle_DeduccionesViewSet(viewsets.ModelViewSet):
    queryset = Detalle_Deducciones.objects.all()
    serializer_class = Detalle_DeduccionesSerializer

    # metodo create
    def create(self, request, *args, **kwargs):
        id_contrato = request.data.get('id_contrato')
        id_deducciones = request.data.get('id_deducciones')

        if Detalle_Deducciones.objects.filter(id_contrato=id_contrato, id_deducciones=id_deducciones,
                                             is_active=True).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="La deducción que intenta asociar ya esta enlazado a este contrato",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Detalle de deducción creado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_201_CREATED)

    #METODO LIST POR CONTRATO
    def list(self, request, *args, **kwargs):
        codigo_contrato = request.data.get('codigo')

        if codigo_contrato:
            contratos = Contrato.objects.filter(codigo_contrato=codigo_contrato, is_active = True)

            if contratos.exists():
                queryset = Detalle_Deducciones.objects.filter(id_contrato__in=contratos, is_active=True)
                if not queryset.exists():
                    return Response({
                        "Success": True,
                        "Status": status.HTTP_204_NO_CONTENT,
                        "Message": f"El contrato con código {codigo_contrato} no tiene deducciones asociadas",
                        "Record": None
                    }, status=status.HTTP_200_OK)
                message = f"Detalles de deducciones asociados al contrato con código: {codigo_contrato}"
            else:
                return Response({
                    "Success": False,
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "Contrato no encontrado",
                    "Record": None
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Detalle_Deducciones.objects.filter(is_active=True)
            message = "Lista completa de detalles de deducciones activos"

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "Success": True,
            "Status": status.HTTP_200_OK,
            "Message": message,
            "Record": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

# Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-detalle-deduccion')
    def eliminar_detalle(self, request):
        id_deduccion = request.data.get('id_deduccion')

        if not id_deduccion:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="ID no proporcionado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        deduccion = Detalle_Deducciones.objects.filter(id_detalle_deduciones=id_deduccion, is_active=True).first()

        if not deduccion:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f'No hay un detalle de deducción activo con el ID: {id_deduccion}',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        deduccion.is_active = False
        deduccion.save()
        serializer = self.get_serializer(deduccion)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Detalle de deducción eliminada con éxito.',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    #Modificar
    @action(detail=False, methods=['put'], url_path='modificar-detalle')
    def modificar_detalle(self, request):
        id_detalle = request.data.get('id_detalle_deducciones')
        if not id_detalle:
            data_response =ResponseData(
                Success= False,
                Status= status.HTTP_400_BAD_REQUEST,
                Message= "Proporcione el ID del detalle que desea modificar",
                Record= None
            )
            return Response(data_response.toResponse(), status= status.HTTP_400_BAD_REQUEST)
        detalle = Detalle_Deducciones.objects.filter(id_detalle_deduciones = id_detalle, is_active = True).first()

        if not detalle:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message=f"No hay un detalle de deducción con el ID: {id_detalle}",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = Detalle_DeduccionesSerializer(detalle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Detalle de deducción actualizado con éxito",
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


