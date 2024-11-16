from Deducciones_.deducciones.API.API_Deducciones import DeduccionesViewSet
from rest_framework.routers import DefaultRouter

routerDeducciones = DefaultRouter()
routerDeducciones.register('deducciones', DeduccionesViewSet)