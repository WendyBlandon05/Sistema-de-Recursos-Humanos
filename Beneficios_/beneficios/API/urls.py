from rest_framework.routers import DefaultRouter
from Beneficios_.beneficios.API.API_Beneficios import BeneficiosViewset

routerBeneficios = DefaultRouter()
#Registro de viewset tipo BENEFICiOS
routerBeneficios.register(r'beneficios', BeneficiosViewset)

