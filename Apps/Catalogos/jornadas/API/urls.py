from rest_framework.routers import DefaultRouter
from Apps.Catalogos.jornadas.API.API_Jornadas import JornadaViewSet

routerJornada = DefaultRouter()
routerJornada.register('jornada', JornadaViewSet)