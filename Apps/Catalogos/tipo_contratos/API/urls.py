from rest_framework.routers import DefaultRouter
from Apps.Catalogos.tipo_contratos.API.API_Tipo_Contratos import Tipo_ContratoViewSet

routerTipoContrato = DefaultRouter()
routerTipoContrato.register('tipo-contratos', Tipo_ContratoViewSet)