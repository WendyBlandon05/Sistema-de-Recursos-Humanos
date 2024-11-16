from rest_framework.routers import DefaultRouter
from Beneficios_.detalle_beneficios.API.API_Detalle_Beneficios import Detalle_BeneficioViewSet

routerDetalleBeneficio = DefaultRouter()
routerDetalleBeneficio.register('detalle-beneficios', Detalle_BeneficioViewSet)