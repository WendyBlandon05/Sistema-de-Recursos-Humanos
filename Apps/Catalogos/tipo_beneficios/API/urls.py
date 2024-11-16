from rest_framework.routers import DefaultRouter
from Apps.Catalogos.tipo_beneficios.API.API_Tipo_Beneficios import Tipo_BeneficiosViewSet

routerTipoBeneficio = DefaultRouter()
routerTipoBeneficio.register('tipo-beneficios', Tipo_BeneficiosViewSet)