from rest_framework.routers import DefaultRouter
from Apps.Catalogos.tipo_deducciones.API.API_Tipo_Deducciones import Tipo_DeduccionesViewSet

routerTipoDeducciones = DefaultRouter()
routerTipoDeducciones.register('tipo-deducciones', Tipo_DeduccionesViewSet)