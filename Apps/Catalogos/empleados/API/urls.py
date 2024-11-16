from Apps.Catalogos.empleados.API.API_Empleados import EmpleadoViewSet
from rest_framework.routers import DefaultRouter

routerEmpleado = DefaultRouter()
routerEmpleado.register('empleado', EmpleadoViewSet)