from rest_framework.routers import DefaultRouter
from Nomina_.nominas.API.API_Nominas import NominaViewSet

routerNomina = DefaultRouter()
routerNomina.register('nomina', NominaViewSet)