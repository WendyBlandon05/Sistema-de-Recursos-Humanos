from rest_framework.routers import DefaultRouter
from Contratacion_.contratos.API.API_Contratos import ContratoViewSet

routerContratos = DefaultRouter()

routerContratos.register('contratos', ContratoViewSet)