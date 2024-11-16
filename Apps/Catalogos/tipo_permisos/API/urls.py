from rest_framework.routers import DefaultRouter
from Apps.Catalogos.tipo_permisos.API.API_Tipo_Permisos import TipoPermisoViewSet

routerTipoPermisos = DefaultRouter()
routerTipoPermisos.register('tipo-permisos', TipoPermisoViewSet)