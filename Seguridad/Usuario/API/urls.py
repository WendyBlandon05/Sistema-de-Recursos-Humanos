from Seguridad.Usuario.API.API import UsuarioCreateView
from django.urls import path


urlpatterns = [
    path('api/v1/register/', UsuarioCreateView.as_view(), name='register-user'),
]