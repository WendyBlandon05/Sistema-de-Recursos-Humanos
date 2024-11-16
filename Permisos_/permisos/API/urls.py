from rest_framework.routers import DefaultRouter
from Permisos_.permisos.API.API_Permisos import PermisoViewSet

routerPermisos = DefaultRouter()
routerPermisos.register('permisos', PermisoViewSet)