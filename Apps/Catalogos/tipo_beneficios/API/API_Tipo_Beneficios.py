from rest_framework import viewsets, status
from Apps.Catalogos.tipo_beneficios.models import Tipo_Beneficios
from Apps.Catalogos.tipo_beneficios.API.serializers import Tipo_BeneficiosSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from Utils.ResposeData import ResponseData

class Tipo_BeneficiosViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Beneficios.objects.all()
    serializer_class = Tipo_BeneficiosSerializer

    # Cambiar nombre de un beneficio
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
        if len(nuevo_nombre.strip()) < 3:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El nuevo nombre debe tener al menos 3 caracteres y no debe contener solo espacios.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        beneficios =Tipo_Beneficios.objects.filter(nombre_beneficio=nombre_actual, is_active=True).first()
        if not beneficios:
            response_data = ResponseData(
                Success= False,
                Status= status.HTTP_404_NOT_FOUND,
                Message="No hay un tipo de beneficio con ese nombre",
                Record= None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        beneficios.nombre_beneficio = nuevo_nombre
        beneficios.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Nombre actualizado con éxito',
            Record={
                "id":beneficios.id_tipo_beneficios,
                "nombre_tipo_beneficios":beneficios.nombre_beneficio
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)


    # Sobreescribir metodo create
    def create(self, request, *args, **kwargs):
        nombre_beneficio = request.data.get('nombre_beneficio')

        if Tipo_Beneficios.objects.filter(nombre_beneficio=nombre_beneficio, is_active=True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Ya existe un tipo de beneficio con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='Tipo de beneficio creado',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)


    # Sobreescribir metodo LIST
    def list(self, request, *args, **kwargs):
        nombre_beneficio = request.data.get('nombre_beneficio') or request.GET.get('nombre_beneficio')

        if nombre_beneficio:
            queryset = Tipo_Beneficios.objects.filter(nombre_beneficio=nombre_beneficio, is_active=True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message= "No hay un tipo de beneficios con ese nombre",
                    Record= None
                )
                return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                message= f"Coincidencia encontrada con: {nombre_beneficio}"
        else:
            queryset = Tipo_Beneficios.objects.filter(is_active = True)
            message = "Lista completa de Tipo de beneficios"

        serializer = self.get_serializer(queryset, many=True)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Eliminar por nombre
    @action(detail=False, methods=['Delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_beneficio = request.data.get('nombre_beneficio')

        if not nombre_beneficio:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Nombre de beneficio no proporcionado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        beneficio = Tipo_Beneficios.objects.filter(nombre_beneficio=nombre_beneficio, is_active=True).first()

        if not beneficio:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='No hay un tipo de beneficio con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        beneficio.is_active = False
        beneficio.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Tipo de beneficio eliminado con éxito.',
            Record={
                "id": beneficio.id_tipo_beneficios,
                "nombre_beneficio": beneficio.nombre_beneficio,
                "is_active": beneficio.is_active
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)
