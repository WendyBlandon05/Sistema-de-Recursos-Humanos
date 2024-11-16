from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Contratacion_.documentos_personales.models import documentos_personales
from Contratacion_.documentos_personales.API.serializers import Documentos_PersonalesSerializer
from Apps.Catalogos.empleados.models import Empleado
from Utils.ResposeData import ResponseData

class Documentos_PersonalesViewSet(viewsets.ModelViewSet):
    queryset = documentos_personales.objects.all()
    serializer_class = Documentos_PersonalesSerializer

    #Metodo list por cedula del empleado
    def list(self, request, *args, **kwargs):
        numero_cedula = request.data.get('numero_cedula')

        if numero_cedula:
            empleados = Empleado.objects.filter(numero_cedula=numero_cedula, is_active=True)

            if empleados.exists():
                queryset = documentos_personales.objects.filter(id_empleados__in=empleados, is_active=True)
                if not queryset.exists():
                    data_response=ResponseData(
                        Success= True,
                        Status= status.HTTP_204_NO_CONTENT,
                        Message="El numero de cedula del empleado no tiene ningun documento asociado",
                        Record=None
                    )
                    return Response(data_response.toResponse(), status=status.HTTP_200_OK)
                message = f"Documentos asociados al empleado con número de cédula: {numero_cedula}"
            else:
                data_response = ResponseData(
                    Success=True,
                    Status=status.HTTP_204_NO_CONTENT,
                    Message="No hay un empleado con ese número de cédula.",
                    Record=None
                )
                return Response(data_response.toResponse(), status=status.HTTP_200_OK)
        else:
            queryset = documentos_personales.objects.filter(is_active=True)
            message = "Lista completa de documentos personales registrados"

        serializer = self.get_serializer(queryset, many=True)
        data_response = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(data_response.toResponse(), status=status.HTTP_200_OK)

    #CREATE DOCUMENTS
    def create(self, request, *args, **kwargs):
        documentos = request.data

        serializer = Documentos_PersonalesSerializer(data=documentos)

        if serializer.is_valid():
            detalle = serializer.save()

            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_201_CREATED,
                Message="Deocumento guarado exitosamente.",
                Record=serializer.data
            )
            return Response(data_response.toResponse(), status=status.HTTP_201_CREATED)

        data_response = ResponseData(
            Success=False,
            Status=status.HTTP_400_BAD_REQUEST,
            Message="Errores de validación.",
            Record=serializer.errors
        )
        return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

 #DELETE FOR ID
    @action(detail=False, methods=['delete'], url_path='eliminar-documento')
    def eliminar_documento(self, request):
        id = request.data.get('id_documento')

        if not id:
            data_response = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Proporcione el ID del documento que desea eliminar",
                Record=None)
            return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        try:
            detalle = documentos_personales.objects.filter(id_documentos_personales=id, is_active=True).first()
            if not detalle:
                data_response = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message=f"No hay un documento con el ID:{id} ",
                    Record=None)
                return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

            detalle.is_active = False
            detalle.save()
            serializer = self.get_serializer(detalle)

            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Documento eliminado exitosamente.",
                Record=serializer.data
            )
            return Response(data_response.toResponse(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el documento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #UPDATE FOR PRIMARY KEY
    @action(detail=False, methods=['put'], url_path='actualizar-documento')
    def actualizar_documento(self, request):
        id_documento = request.data.get('id_documento')
        if not id_documento:
            return Response({
                "Success": False,
                "Status": status.HTTP_400_BAD_REQUEST,
                "Message": "El ID del documento es obligatorio.",
                "Record": None
            }, status=status.HTTP_400_BAD_REQUEST)

        detalle = documentos_personales.objects.filter(id_documentos_personales=id_documento, is_active=True).first()

        if not detalle:
            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="No hay documento con ese ID.",
                Record=None
            )
            return Response(data_response.toResponse(), status=status.HTTP_200_OK)


        serializer = Documentos_PersonalesSerializer(detalle, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Documento actualizado exitosamente.",
                Record=serializer.data
            )
            return Response(data_response.toResponse(), status=status.HTTP_200_OK)

        data_response = ResponseData(
            Success=False,
            Status=status.HTTP_400_BAD_REQUEST,
            Message="Errores de validación.",
            Record=serializer.errors
        )
        return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)






