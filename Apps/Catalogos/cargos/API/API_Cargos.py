from rest_framework.decorators import action
from rest_framework.response import Response
from Utils.ResposeData import ResponseData
from Apps.Catalogos.cargos.API.serializers import CargosSerializer
from rest_framework import viewsets, status
from Apps.Catalogos.cargos.models import Cargos

class CargosViewSet(viewsets.ModelViewSet):
    queryset = Cargos.objects.all()
    serializer_class = CargosSerializer

    # Cambiar nombre de cargo
    @action(detail=False, methods=['patch'], url_path='cambiar-nombre')
    def cambiar_nombre(self, request):
        # Obtener el nombre actual y el nuevo desde Postman
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
                Message="El nuevo nombre debe tener al menos 4 caracteres y no debe contener solo espacios.",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        if Cargos.objects.filter(nombre_cargo=nuevo_nombre, is_active=True).exclude(
                nombre_cargo=nombre_actual).exists():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe un cargo con ese nombre digite uno diferente",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        cargo = Cargos.objects.filter(nombre_cargo=nombre_actual, is_active=True).first()
        if not cargo:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="No hay un cargo con ese nombre",
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        cargo.nombre_cargo = nuevo_nombre
        cargo.save()

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Nombre actualizado con éxito',
            Record={
                "id":cargo.id_cargos,
                "nombre_cargo": cargo.nombre_cargo,
                "salario_base": cargo.salario_base
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

    # Sobreescribir
    def create(self, request, *args, **kwargs):
        nombre_cargo = request.data.get('nombre_cargo')

        if Cargos.objects.filter(nombre_cargo=nombre_cargo, is_active=True).exists():
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Ya existe un cargo con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message='Cargo creado con éxito',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_201_CREATED)

    # Sobreescribir list
    def list(self, request, *args, **kwargs):
        nombre_cargo = request.data.get('nombre_cargo') or request.GET.get('nombre_cargo')

        if nombre_cargo:
            queryset = Cargos.objects.filter(nombre_cargo=nombre_cargo, is_active=True)
            if not queryset.exists():
                response_data = ResponseData(
                    Success= False,
                    Status= status.HTTP_404_NOT_FOUND,
                    Message= "No hay un beneficios con ese nombre",
                    Record= None
                )
                return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
            else:
                mensaje = f"Coincidencia encontrada con {nombre_cargo}"
        else:
            queryset = Cargos.objects.filter(is_active = True)
            mensaje = "Lista de todos los cargos disponibles"

        serializer = self.get_serializer(queryset, many=True)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=mensaje,
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_200_OK)


    # Actualizar por nombre de cargo
    @action(detail=False, methods=['put'], url_path='actualizar-cargo')
    def actualizar_por_nombre(self, request):
        nombre_cargo = request.data.get('nombre_cargo')
        cargo = Cargos.objects.filter(nombre_cargo=nombre_cargo, is_active = True).first()
        if not cargo:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='Cargo no encontrado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = CargosSerializer(cargo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message='Cargo actualizado con éxito',
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

    # Eliminar por nombre
    @action(detail=False, methods=['delete'], url_path='eliminar-nombre')
    def eliminar_nombre(self, request):
        nombre_cargo = request.data.get('nombre_cargo')

        # Verificar si el cargo existe y está activo
        cargo = Cargos.objects.filter(nombre_cargo=nombre_cargo, is_active=True).first()

        if not cargo:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='No hay un cargo activo con ese nombre',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        cargo.is_active = False
        cargo.save()
        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Cargo eliminado con éxito.',
            Record={
                "id": cargo.id_cargos,
                "nombre_cargo": cargo.nombre_cargo,
                "is_active": cargo.is_active
            }
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)

#ACTION DE PRUEBA
    @action(detail=False, methods=['get'], url_path='listar-por-salario')
    def listar_por_salario(self, request):
        salario = request.data.get('salario') or request.GET.get('salario')

        if salario is None:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Salario no proporcionado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        try:
            salario = float(salario)
        except ValueError:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message='Salario inválido',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        cargos = Cargos.objects.filter(salario_base=salario, is_active=True)
        if not cargos:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message='No se encontraron cargos con el salario especificado',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = CargosSerializer(cargos, many=True)
        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message=f'Cargos con coincidencia con el salario: {salario}',
            Record=serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)