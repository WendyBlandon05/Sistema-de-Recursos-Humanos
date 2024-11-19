from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Contratacion_.contratos.models import Contrato
from Nomina_.detalle_nomina.API.serializers import Detalle_NominaSerializer
from Nomina_.detalle_nomina.models import Detalle_Nomina
from Utils.ResposeData import ResponseData
from django.db import connection
from django.db import transaction
import openpyxl

class Detalle_NominaViewSet(viewsets.ModelViewSet):
    queryset = Detalle_Nomina.objects.all()
    serializer_class = Detalle_NominaSerializer

    @action(detail=False, methods=['post'], url_path='calcular-detalles-nomina')
    def calcular_detalles(self, request):
        mes_pagado = request.data.get("mes_pagado")
        if not mes_pagado:
            data_response = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Falta el mes para calcular la nómina",
                Record=None
            )
            return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        # Define la consulta SQL para ejecutar el procedimiento almacenado
        query = "EXEC USP_CalcularDetalleNomina @mes_pagado = %s"

        try:
            # Ejecutar la consulta con mis parametros del request
            with connection.cursor() as cursor:
                cursor.execute(query, [mes_pagado,])
                resultados = cursor.fetchall()

            # Organizacion a Jeisito :)
            datos = [
                {
                    "id_nomina": row[0],
                    "id_contrato": row[1],
                    "salario_bruto": row[2],
                    "salario_neto": row[3],
                    "monto_beneficios": row[4],
                    "monto_deducciones": row[5]
                }
                for row in resultados
            ]

            return Response(datos)

        except Exception as e:
            print("Error al ejecutar la consulta:", e)
            return Response({"error": str(e)}, status=500)

#PRUEBA DE MEtODO DE INSERCION EN LISTA
    @action(detail=False, methods=['post'], url_path='insertar-detalles-nomina')
    def insertar_detalles_nomina(self, request):
        lista_detalles = request.data

        if not isinstance(lista_detalles, list):
            data_response = ResponseData(
                Success= False,
                Status= status.HTTP_400_BAD_REQUEST,
                Message="Error, debe pasar una lista de todos los detales",
                Record=None
            )
            return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)


        try:
            with transaction.atomic():
                detalles_a_guardar = []
                for detalle_data in lista_detalles:
                    #Validar los datos de cada detalle
                    serializer = Detalle_NominaSerializer(data=detalle_data)
                    if serializer.is_valid():
                #Si son se validos todos se guardanm
                        detalles_a_guardar.append(Detalle_Nomina(**serializer.validated_data))
                    else:
                        data_response = ResponseData(
                            Success=False,
                            Status=status.HTTP_400_BAD_REQUEST,
                            Message= "ERRORES: Revise los detalles a insertar, no cumplen con los párametros de validación",
                            Record=None
                        )
                        return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

                # Insertar los detalles
                Detalle_Nomina.objects.bulk_create(detalles_a_guardar)
                serializer = self.get_serializer(detalles_a_guardar, many=True)
                data_response = ResponseData(
                    Success= True,
                    Status=status.HTTP_201_CREATED,
                    Message= "Todos los detalles de nómina se han insertado exitosamente.",
                    Record=serializer.data
                )
            return Response( data_response.toResponse(),
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"Error al insertar los registros: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    #ELIMINAR DETALLE POR PRIMARY KEY
    @action(detail=False, methods=['delete'], url_path='eliminar-detalle')
    def eliminar_detalle(self, request):
        id = request.data.get('id_detalle')

        if not id:
            data_response = ResponseData(
                Success= False,
                Status= status.HTTP_400_BAD_REQUEST,
                Message="Proporcione el ID del detalle que desea eliminar",
                Record= None)
            return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

        try:
            detalle = Detalle_Nomina.objects.filter(id_detalle_nomina=id, is_active = True).first()
            if not detalle:
                data_response = ResponseData(
                    Success=False,
                    Status=status.HTTP_400_BAD_REQUEST,
                    Message=f"No hay un detalle de nómina con el ID:{id} ",
                    Record=None)
                return Response(data_response.toResponse(), status=status.HTTP_400_BAD_REQUEST)

            detalle.is_active = False
            detalle.save()
            serializer = self.get_serializer(detalle)

            # Respuesta exitosa
            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Detalle de nómina eliminado exitosamente.",
                Record=serializer.data
            )
            return Response(data_response.toResponse(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el detalle: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


        #LISTAR DETALLES DE NOMINAS MEDIANTE CODIGO DE CONTRATO, O POR DEFAULT
    def list(self, request, *args, **kwargs):
        codigo_contrato = request.data.get('codigo')

        if codigo_contrato:
            contratos = Contrato.objects.filter(codigo_contrato=codigo_contrato, is_active=True)

            if contratos.exists():
                queryset = Detalle_Nomina.objects.filter(id_contrato__in=contratos, is_active=True)
                if not queryset.exists():
                    return Response({
                        "Success": True,
                        "Status": status.HTTP_204_NO_CONTENT,
                        "Message": f"El contrato con código {codigo_contrato} no tiene nóminas asociados",
                        "Record": None
                    }, status=status.HTTP_200_OK)
                message = f"Detalles de nómina asociados al contrato con código {codigo_contrato}"
            else:
                return Response({
                    "Success": False,
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "Contrato no encontrado",
                    "Record": None
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Detalle_Nomina.objects.filter(is_active=True)
            message = "Lista completa de detalles de nóminas"

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "Success": True,
            "Status": status.HTTP_200_OK,
            "Message": message,
            "Record": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['put'], url_path='actualizar-detalle')
    def actualizar_detalle(self, request):
        id_detalle = request.data.get('id_detalle_nomina')
        if not id_detalle:
            return Response({
                "Success": False,
                "Status": status.HTTP_400_BAD_REQUEST,
                "Message": "El ID del detalle de nómina es obligatorio.",
                "Record": None
            }, status=status.HTTP_400_BAD_REQUEST)

        detalle = Detalle_Nomina.objects.filter(id_detalle_nomina=id_detalle, is_active=True).first()

        if not detalle:
            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="No hay detalle con ese ID.",
                Record=None
            )
            return Response(data_response.toResponse(), status=status.HTTP_200_OK)


        serializer = Detalle_NominaSerializer(detalle, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data_response = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Detalle de nómina actualizado exitosamente.",
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


    # INTENTO DE GENERAR REPORTE EN EXCEL
    @action(detail=False, methods=['post'], url_path='reporte')
    def generar_reporte(self, request):
        id_nomina = request.data.get("id_nomina") or request.GET.get("id_nomina")

        if id_nomina:
            detalles = Detalle_Nomina.objects.filter(id_nomina=id_nomina, is_active=True)
            if not detalles:
                response_data = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message="No hay detalles de nómina asociados al id enviado",
                    Record=None
                )
                return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)
        else:
            detalles = Detalle_Nomina.objects.filter(is_active=True)

        # Crear el archivo Excel
        workbook = openpyxl.Workbook()
        hoja = workbook.active
        hoja.title = "Detalles de nómina"
        hoja.append(["id_detalle_nomina", "id_nomina", "id_contrato", "salario_bruto", "salario_neto", "monto_beneficios",
                     "monto_deducciones"])

        for detalle in detalles:
            hoja.append([detalle.id_detalle_nomina, detalle.id_nomina.id_nomina, detalle.id_contrato.id_contratos,
                         detalle.salario_bruto, detalle.salario_neto, detalle.monto_beneficios, detalle.monto_deducciones])

        # Crear la respuesta como archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=detalles_nomina.xlsx'

        # Guardar el archivo Excel en la respuesta HTTP
        workbook.save(response)

        # Retornar la respuesta
        return response

#intento mil de un pdf:(
    @action(detail=False, methods=['post'], url_path='reporte-pdf')
    def generar_reporte_pdf(self, request):
        id_nomina = request.data.get("id_nomina") or request.GET.get("id_nomina")

        if id_nomina:
            detalles = Detalle_Nomina.objects.filter(id_nomina=id_nomina, is_active=True)
            if not detalles:
                response_data = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message="No hay detalles de nómina asociados al id enviado",
                    Record=None
                )
                return Response(response_data.toResponse(), status=status.HTTP_404_NOT_FOUND)
        else:
            detalles = Detalle_Nomina.objects.filter(is_active=True)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        #encabezados que va a llevar la table
        encabezados = ["ID Detalle Nómina", "ID Nómina", "ID Contrato", "Salario Bruto", "Salario Neto",
                       "Monto Beneficios", "Monto Deducciones"]

        data = [encabezados]
        for detalle in detalles:
            data.append([
                str(detalle.id_detalle_nomina),
                str(detalle.id_nomina.id_nomina),
                str(detalle.id_contrato.id_contratos),
                str(detalle.salario_bruto),
                str(detalle.salario_neto),
                str(detalle.monto_beneficios),
                str(detalle.monto_deducciones),
            ])
        table = Table(data)

        #personalizacion de la tabla
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (0.5, 0.5, 0.5)),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),
            ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        elements = [table]


        def agregar_encabezado(canvas, doc):
            canvas.setFont("Helvetica-Bold", 16)
            canvas.drawString(200, 750, "Reporte de Detalles de Nómina")

            canvas.setFont("Helvetica", 12)
            canvas.drawString(200, 730,
                              "Reporte generado para la nómina ID: {}".format(id_nomina if id_nomina else "lISTA DE DETALLES EXISTENTES"))

            canvas.drawString(200, 710, " ")

        doc.build(elements, onFirstPage=agregar_encabezado)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=detalles_nomina.pdf'

        return response