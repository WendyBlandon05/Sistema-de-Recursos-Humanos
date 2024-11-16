from rest_framework.permissions import BasePermission

from Apps.Catalogos.empleados.models import Empleado


class PuedeVerEmpleado(BasePermission):

    def has_permission(self, request, view):
        cedula_usuario = request.user.numero_cedula

        if view.action == 'list':
            empleados = Empleado.objects.filter(numero_cedula=cedula_usuario)
            return empleados.exists()

        return False
