from rest_framework.routers import DefaultRouter
from Nomina_.detalle_nomina.API.API_Detalle_Nomina import Detalle_NominaViewSet

routerDetalleNomina = DefaultRouter()
routerDetalleNomina.register('detalle-nomina', Detalle_NominaViewSet)