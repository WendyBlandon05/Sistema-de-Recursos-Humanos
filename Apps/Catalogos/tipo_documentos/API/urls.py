from rest_framework.routers import DefaultRouter
from Apps.Catalogos.tipo_documentos.API.API_Tipo_Documentos import Tipo_DocumentosViewSet

routerTipoDocumentos = DefaultRouter ()
routerTipoDocumentos.register('tipo-documentos', Tipo_DocumentosViewSet)
