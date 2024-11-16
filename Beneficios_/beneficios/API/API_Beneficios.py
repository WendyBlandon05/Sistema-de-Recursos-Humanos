from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Beneficios_.beneficios.API.serializers import BeneficiosSerializer
from Beneficios_.beneficios.models import Beneficios
from Utils.ResposeData import ResponseData

class BeneficiosViewset(viewsets.ModelViewSet):
    queryset = Beneficios.objects.all()
    serializer_class = BeneficiosSerializer

# Cambiar nombre de un beneficio
    @action(detail=False, methods=['patch'], url_path='cambiar-nombre')
    def cambiar_nombre(self, request):
        nombre_actual = request.data.get('nombre_actual')
        nuevo_nombre = request.data.get('nuevo_nombre')

        if not nombre_actual or not nuevo_nombre:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre actual o nuevo no proporcionado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if len(nuevo_nombre.strip()) < 4:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El nuevo nombre debe tener al menos 4 caracteres y no debe contener solo espacios.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if Beneficios.objects.filter(nombre_beneficio=nuevo_nombre, is_active=True).exclude(
                nombre_beneficio=nombre_actual).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un beneficio con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        beneficio =Beneficios.objects.filter(nombre_beneficio=nombre_actual, is_active=True).first()
        if not beneficio:
            response_data = ResponseData(
                Success= False,
                Status= status.HTTP_404_NOT_FOUND,
                Message="No hay un beneficio con ese nombre",
                Record= None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        beneficio.nombre_beneficio = nuevo_nombre
        beneficio.save()
        serializer = self.get_serializer(beneficio)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Nombre actualizado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # metodo create
    def create(self, request, *args, **kwargs):
        nombre_beneficio = request.data.get('nombre_beneficio')

        # Verificar si ya existe
        if Beneficios.objects.filter(nombre_beneficio=nombre_beneficio, is_active= True).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un beneficio con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Beneficio creado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir metodo list
    def list(self, request, *args, **kwargs):
        nombre_beneficio = request.data.get('nombre_beneficio') or request.GET.get('nombre_beneficio')

        if nombre_beneficio:
            queryset = Beneficios.objects.filter(nombre_beneficio=nombre_beneficio, is_active= True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message= "No hay un beneficios con ese nombre",
                    Record= None
                )
                return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                message= f"Coincidencia encontrada con: {nombre_beneficio}"
        else:
            queryset = Beneficios.objects.filter(is_active=True)
            message = "Lista completa de beneficios"

        serializer = self.get_serializer(queryset, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # Actualizar por nombre de beneficio
    @action(detail=False, methods=['put'], url_path='actualizar-beneficio')
    def actualizar_por_nombre(self, request):
        nombre_beneficio = request.data.get('nombre_beneficio')

        beneficio = Beneficios.objects.filter(nombre_beneficio=nombre_beneficio, is_active= True).first()

        if not beneficio:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Beneficio no encontrado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = BeneficiosSerializer(beneficio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Beneficio actualizado con éxito",
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

    # Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_beneficio = request.data.get('nombre_beneficio')

        if not nombre_beneficio:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Nombre de beneficio no proporcionado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        beneficio = Beneficios.objects.filter(nombre_beneficio=nombre_beneficio, is_active=True).first()

        if not beneficio:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="No hay un beneficio con ese nombre",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        beneficio.is_active = False
        beneficio.save()
        serializer = self.get_serializer(beneficio)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Beneficio eliminado con éxito.",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)
#Listar por tipo de beneficio