"""
URL configuration for Config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Documentación de las APIS de AdminRH",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="wblandon05@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def index(request):
    return HttpResponse("Página de inicio del sistema AdminRH")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminrh/', include('Apps.Catalogos.urls')),
    path('', index),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),




    # Ruta para obtener un nuevo token JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Ruta para refrescar el token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
