from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Permisos_.detalle_permiso.API.serializers import Detalle_PermisoSerializer
from Permisos_.detalle_permiso.models import Detalle_permiso
from Apps.Catalogos.empleados.models import Empleado
from Utils.ResposeData import ResponseData

class Detalle_PermisoViewSet(viewsets.ModelViewSet):
    queryset = Detalle_permiso.objects.all()
    serializer_class = Detalle_PermisoSerializer

    def create(self, request, *args, **kwargs):
        detalle_data = request.data

        serializer = Detalle_PermisoSerializer(data=detalle_data)

        if serializer.is_valid():
            detalle = serializer.save()

            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_201_CREATED,
                Message="Detalle de permiso creado exitosamente.",
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

    def list(self, request, *args, **kwargs):
        cedula = request.data.get('cedula_empleado')

        if cedula:
            empleado = Empleado.objects.filter(numero_cedula=cedula, is_active=True)

            if empleado.exists():
                queryset = Detalle_permiso.objects.filter(id_empleados__in=empleado, is_active=True)
                if not queryset.exists():
                    data_response = ResponseData(
                        Success=True,
                        Status=status.HTTP_204_NO_CONTENT,
                        Message=f"El empleado con cédula: {cedula} no tiene detalles de permisos asociados",
                        Record=None
                    )
                    return Response(data_response.toResponse(), status=status.HTTP_200_OK)
                message = f"Detalles de nómina asociados al empleado con cédula: {cedula}"
            else:
                data_response = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message="Empleado no encontrado",
                    Record=None
                )
                return Response(data_response.toResponse(), status=status.HTTP_404_NOT_FOUND)

        else:
            queryset = Detalle_permiso.objects.filter(is_active=True)
            message = "Lista completa de detalles de permisos"

        serializer = self.get_serializer(queryset, many=True)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    #DELETE FOR ID
    @action(detail=False, methods=['delete'], url_path='eliminar-detalle')
    def eliminar_detalle(self, request):
        id = request.data.get('id_detalle')

        if not id:
            data_response = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Proporcione el ID del detalle de permiso que desea eliminar",
                Record=None)
            return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        try:
            detalle = Detalle_permiso.objects.filter(id_detalle_permisos=id, is_active=True).first()
            if not detalle:
                data_response = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message=f"No hay un detalle de permiso con el ID:{id} ",
                    Record=None)
                return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

            detalle.is_active = False
            detalle.save()
            serializer = self.get_serializer(detalle)

            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Detalle de permiso eliminado exitosamente.",
                Record=serializer.data
            )
            return Response(data_response.toResponse(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el detalle: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #UPDATE FOR PRIMARY KEY
    @action(detail=False, methods=['put'], url_path='actualizar-detalle')
    def actualizar_detalle(self, request):
        id_detalle = request.data.get('id_detalle')
        if not id_detalle:
            return Response({
                "Success": False,
                "Status": status.HTTP_400_BAD_REQUEST,
                "Message": "El ID del detalle de permiso es obligatorio.",
                "Record": None
            }, status=status.HTTP_400_BAD_REQUEST)

        detalle = Detalle_permiso.objects.filter(id_detalle_permisos=id_detalle, is_active=True).first()

        if not detalle:
            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="No hay detalle con ese ID.",
                Record=None
            )
            return Response(data_response.toResponse(), status=status.HTTP_200_OK)


        serializer = Detalle_PermisoSerializer(detalle, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Detalle de permiso actualizado exitosamente.",
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


