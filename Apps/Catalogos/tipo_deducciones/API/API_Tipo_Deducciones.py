
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Utils.ResposeData import ResponseData
from Apps.Catalogos.tipo_deducciones.models import Tipo_Deducciones
from Apps.Catalogos.tipo_deducciones.API.serializers import Tipo_DeduccionesSerializer

class Tipo_DeduccionesViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Deducciones.objects.all()
    serializer_class = Tipo_DeduccionesSerializer

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

        deduccion = Tipo_Deducciones.objects.filter(nombre_tipo_deducciones=nombre_actual, is_active = True).first()
        if not deduccion:
            response_data = ResponseData(
                Success=False,
                Status = status.HTTP_404_NOT_FOUND,
                Message= "No hay coincidencias con el nombre proporcionado",
                Record= None
            )
            return Response(response_data.toResponse(),status=status.HTTP_404_NOT_FOUND)

        deduccion.nombre_tipo_deducciones = nuevo_nombre
        deduccion.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Nombre actualizado con éxito",
            Record={
                "id": deduccion.id_tipo_deducciones,
                "nombre_tipo_deducciones": deduccion.nombre_tipo_deducciones
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Sobreescribir metodo create
    def create(self, request, *args, **kwargs):
        nombre_tipo_deducciones = request.data.get('nombre_tipo_deducciones')

        if Tipo_Deducciones.objects.filter(nombre_tipo_deducciones=nombre_tipo_deducciones, is_active=True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un tipo de deducción con ese nombre",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Tipo de deducción creado",
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir metodo LIST
    def list(self, request, *args, **kwargs):
        nombre_tipo_deducciones = request.data.get('nombre_tipo_deducciones') or request.GET.get('nombre_tipo_deducciones')

        if nombre_tipo_deducciones:
            queryset = Tipo_Deducciones.objects.filter(nombre_tipo_deducciones=nombre_tipo_deducciones, is_active=True)
            if not queryset.exists():
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message=f"No se encontró ningún tipo de documento con el nombre: {nombre_tipo_deducciones}",
                    Record=None
                )
                return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)
            else:
                message = f"Coincidencia encontrada con: {nombre_tipo_deducciones}"
        else:
            queryset = Tipo_Deducciones.objects.filter(is_active=True)
            message = "Lista completa de tipos de deducciones"

        serializer = self.get_serializer(queryset, many=True)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_tipo_deducciones = request.data.get('nombre_tipo_deducciones')

        if not nombre_tipo_deducciones:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Debe proporcionar un nombre de tipo de deducción válido",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        deduccion = Tipo_Deducciones.objects.filter(nombre_tipo_deducciones=nombre_tipo_deducciones, is_active=True).first()

        if not deduccion:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="No hay un tipo de deducción con ese nombre",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        deduccion.is_active = False
        deduccion.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Tipo de deducción eliminado con éxito",
            Record={
                "id": deduccion.id_tipo_deducciones,
                "nombre_tipo_deducciones": deduccion.nombre_tipo_deducciones,
                "is_active": deduccion.is_active
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)
