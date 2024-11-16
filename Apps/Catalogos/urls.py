from django.urls import path, include
from Beneficios_.beneficios.API.urls import routerBeneficios
from Apps.Catalogos.cargos.API.urls import routerCargos
from Contratacion_.contratos.API.urls import routerContratos
from Deducciones_.deducciones.API.urls import routerDeducciones
from Apps.Catalogos.departamentos.API.urls import routerDepartamento
from Beneficios_.detalle_beneficios.API.urls import routerDetalleBeneficio
from Deducciones_.detalle_deducciones.API.urls import routerDetalleDeducciones
from Nomina_.detalle_nomina.API.urls import routerDetalleNomina
from Permisos_.detalle_permiso.API.urls import routerDetallePermiso
from Contratacion_.documentos_personales.API.urls import routerDocumentosPersonales
from Apps.Catalogos.empleados.API.urls import routerEmpleado
from Contratacion_.historial_contratos.API.urls import routerHistorialContratos
from Apps.Catalogos.jornadas.API.urls import routerJornada
from Nomina_.nominas.API.urls import routerNomina
from Permisos_.permisos.API.urls import routerPermisos
from Apps.Catalogos.tipo_beneficios.API.urls import routerTipoBeneficio
from Apps.Catalogos.tipo_contratos.API.urls import routerTipoContrato
from Apps.Catalogos.tipo_deducciones.API.urls import routerTipoDeducciones
from Apps.Catalogos.tipo_documentos.API.urls import routerTipoDocumentos
from Apps.Catalogos.tipo_permisos.API.urls import routerTipoPermisos

urlpatterns = [
    path('', include(routerBeneficios.urls)),
    path('', include(routerCargos.urls)),
    path('', include(routerContratos.urls)),
    path('', include(routerDeducciones.urls)),
    path('', include(routerDepartamento.urls)),
    path('', include(routerDetalleBeneficio.urls)),
    path('', include(routerDetalleDeducciones.urls)),
    path('', include(routerDetalleNomina.urls)),
    path('', include(routerDetallePermiso.urls)),
    path('', include(routerTipoPermisos.urls)),
    path('', include(routerTipoDocumentos.urls)),
    path('', include(routerTipoDeducciones.urls)),
    path('', include(routerTipoContrato.urls)),
    path('', include(routerTipoBeneficio.urls)),
    path('', include(routerDocumentosPersonales.urls)),
    path('', include(routerEmpleado.urls)),
    path('', include(routerHistorialContratos.urls)),
    path('', include(routerJornada.urls)),
    path('', include(routerNomina.urls)),
    path('', include(routerPermisos.urls)),
    #usuario url prueba
    path('usuarios/', include('Seguridad.Usuario.API.urls')),

]
