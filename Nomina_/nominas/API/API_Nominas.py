from rest_framework import viewsets, status
from rest_framework.response import Response
from Nomina_.nominas.API.serializers import NominaSerializer
from Nomina_.nominas.models import Nomina
from Utils.ResposeData import ResponseData
from django.db import connection
from rest_framework.decorators import action

class NominaViewSet(viewsets.ModelViewSet):
    queryset = Nomina.objects.all()
    serializer_class = NominaSerializer

    @action(detail=False, methods=['post'], url_path='calculo-nomina')
    def post(self, request):
        nombre_empresa = request.data.get("nombre_empresa")
        mes_pagado = request.data.get("mes_pagado")
        estado = request.data.get("estado")
        fecha_pago = request.data.get("fecha_pago")

        if not nombre_empresa or not mes_pagado or not estado or not fecha_pago:
            data_response = ResponseData(
                Success= False,
                Status= status.HTTP_400_BAD_REQUEST,
                Message= "Falta uno o todos los párametros necesarios para calcular la nómina",
                Record= None
            )
            return Response(data_response.toResponse(), status= status.HTTP_400_BAD_REQUEST)

        # Define la consulta SQL para ejecutar el procedimiento almacenado
        query ="EXEC USP_CalcularNomina @nombre_empresa = %s, @mes_pagado = %s, @estado = %s, @fecha_pago = %s"

        try:
            # Ejecutar la consulta con mis parametros del request
            with connection.cursor() as cursor:
                cursor.execute(query, [nombre_empresa, mes_pagado, estado, fecha_pago])
                resultados = cursor.fetchall()

            # Organizacion a Jeisito :)
            datos = [
                {
                    "nombre_empresa": row[0],
                    "mes_pagado": row[1],
                    "estado": row[2],
                    "fecha_pago": row[3],
                    "total_beneficios": row[4],
                    "total_deducciones": row[5],
                    "salario_bruto": row[6],
                    "total_pagar":row[7]
                }
                for row in resultados
            ]

            return Response(datos)

        except Exception as e:
            print("Error al ejecutar la consulta:", e)
            return Response({"error": str(e)}, status=500)


    #SOBREESCRIBIR METODO CREATE
    def create(self, request, *args, **kwargs):
        mes_pagado = request.data.get('mes_pagado')

        # Verificar si ya existe
        if Nomina.objects.filter(mes_pagado=mes_pagado, is_active= True).first():
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Ya existe una nómina con ese mes, agregue el año",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = ResponseData(
            Success=True,
            Status=status.HTTP_201_CREATED,
            Message="Nómina creado con éxito",
            Record=serializer.data
        )
        return Response(data.toResponse(), status=status.HTTP_201_CREATED)


        #ELIMINAR POR MES
    @action(detail=False, methods=['delete'], url_path='eliminar-mes')
    def eliminar_mes(self, request):
        mes = request.data.get('mes_pagado')
        if not mes:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Debe proporcionar un mes para poder eliminar una nómina",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        nomina = Nomina.objects.filter(mes_pagado=mes, is_active=True).first()

        if not nomina:
            response_data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message=f'No hay una nómina asociada al mes {mes}',
                Record=None
            )
            return Response(response_data.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        nomina.is_active = False
        nomina.save()
        serializer = self.get_serializer(nomina)

        response_data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message='Nómina eliminada con éxito.',
            Record= serializer.data
        )
        return Response(response_data.toResponse(), status=status.HTTP_200_OK)
        #LIST
    def list(self, request, *args, **kwargs):
            mes = request.data.get('mes_pagado') or request.GET.get('mes_pagado')
            if mes:
                queryset = Nomina.objects.filter(mes_pagado=mes, is_active=True)
                if not queryset.exists():
                    response_data = ResponseData(
                        Success= False,
                        Status= status.HTTP_404_NOT_FOUND,
                        Message= "No hay una nómina registrada para ese mes",
                        Record= None
                    )
                    return Response(response_data.toResponse(), status= status.HTTP_404_NOT_FOUND)
                else:
                    message= f"Coincidencia encontrada con: {mes}"
            else:
                queryset = Nomina.objects.filter(is_active=True)
                message = "Listas de nóminas activos"

            serializer = self.get_serializer(queryset, many=True)

            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message=message,
                Record=serializer.data
            )
            return Response(data.toResponse(), status=status.HTTP_200_OK)

    #Modificar

    @action(detail=False, methods=['put'], url_path='actualizar-mes')
    def actualizar_por_mes(self, request):
        mes_pagado = request.data.get('mes_pagado')

        nomina = Nomina.objects.filter(mes_pagado=mes_pagado, is_active=True).first()

        if not nomina:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Nómina no encontrado",
                Record=None
            )
            return Response(data.toResponse(), status=status.HTTP_404_NOT_FOUND)

        serializer = NominaSerializer(nomina, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Registro de nómina actualizado con éxito",
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



