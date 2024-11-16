from rest_framework.routers import DefaultRouter
from Apps.Catalogos.cargos.API.API_Cargos import CargosViewSet

routerCargos = DefaultRouter()
routerCargos.register('cargos', CargosViewSet)