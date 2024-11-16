from rest_framework import viewsets, status
from Apps.Catalogos.departamentos.models import Departamento
from Apps.Catalogos.departamentos.API.serializers import DepartamentoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from Utils.ResposeData import ResponseData

class DepartamentosViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

    # Cambiar nombre
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

        if len(nuevo_nombre.strip()) < 4:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="El nuevo nombre del departamento debe contener un minimo de 4 caracteres",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if Departamento.objects.filter(nombre_departamento=nuevo_nombre, is_active=True).exclude(
                nombre_departamento=nombre_actual).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f"Ya existe un departamento con el nombre: {nuevo_nombre}",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        depto = Departamento.objects.filter(nombre_departamento=nombre_actual, is_active = True).first()
        if not depto:
            response_data = ResponseData(
                Success= False,
                Status= status.HTTP_404_NOT_FOUND,
                Message=f"No hay un departamento con el nombre: {nombre_actual}",
                Record= None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        depto.nombre_departamento = nuevo_nombre
        depto.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Nombre actualizado con éxito',
            Record={
                "id":depto.id_departamento,
                "nombre_departamento":depto.nombre_departamento
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)


    # Sobreescribir metodo create
    def create(self, request, *args, **kwargs):
        nombre_departamento = request.data.get('nombre_departamento')

        # Verificar si ya existe
        if Departamento.objects.filter(nombre_departamento=nombre_departamento, is_active=True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Ya existe un departamento con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='Departamento creado con éxito',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)


    # Sobreescribir list
    def list(self, request, *args, **kwargs):
        nombre_depto = request.data.get('nombre_depto') or request.GET.get('nombre_depto')

        if nombre_depto:
            queryset = Departamento.objects.filter(nombre_departamento=nombre_depto, is_active=True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message= f"No existe un departamento con el nombre: {nombre_depto}",
                    Record= None
                )
                return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                message = f"Coincidencia encontrada con {nombre_depto}"
        else:
            queryset = Departamento.objects.filter(is_active=True)
            message = "Lista de departamentos activos"

        serializer = self.get_serializer(queryset, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=message,
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)

    # Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_departamento = request.data.get('nombre_departamento')

        if not nombre_departamento:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Proporcione el nombre del departamento a eliminar",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        depto = Departamento.objects.filter(nombre_departamento=nombre_departamento, is_active=True).first()

        if not depto:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='No hay un departamento con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        depto.is_active = False
        depto.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Departamento eliminado con éxito.',
            Record={
                "id": depto.id_departamento,
                "nombre_departamento": depto.nombre_departamento,
                "is_active": depto.is_active
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)


    # Actualizar por nombre de departamento
    @action(detail=False, methods=['put'], url_path='actualizar-departamento')
    def actualizar_por_nombre(self, request):
        nombre_depto = request.data.get('nombre_depto')

        depto = Departamento.objects.filter(nombre_departamento=nombre_depto, is_active =True).first()

        if not depto:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='Departamento no encontrado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = DepartamentoSerializer(depto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Departamento actualizado con éxito',
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



