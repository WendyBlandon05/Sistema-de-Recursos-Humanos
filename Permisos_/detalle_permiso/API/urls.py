from rest_framework.routers import DefaultRouter
from Permisos_.detalle_permiso.API.API_Detalle_Permiso import Detalle_PermisoViewSet

routerDetallePermiso = DefaultRouter()
routerDetallePermiso.register('detalle-permisos', Detalle_PermisoViewSet)