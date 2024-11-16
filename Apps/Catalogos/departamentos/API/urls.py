from rest_framework.routers import DefaultRouter
from Apps.Catalogos.departamentos.API.API_Departamentos import DepartamentosViewSet

routerDepartamento = DefaultRouter()
routerDepartamento.register('departamentos', DepartamentosViewSet)