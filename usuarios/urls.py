from django.urls import path
from .views import SignUpView, CustomLoginView, carregar_cidades
from .forms import UsuarioLoginForm

app_name = 'usuarios'
from django.contrib.auth import views

from . import views

urlpatterns = [
    path('cadastro', SignUpView.as_view(), name='cadastrousuario'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('perfil/', views.perfil_principal, name='perfil_principal'),
    path('perfil/endereco', views.perfil_endereco, name='perfil_endereco'),
    path('perfil/endereco/adicionar', views.endereco_formulario_adicionar, name='perfil_endereco_adicionar'),
    path('ajax/carregar-cidades/', views.carregar_cidades, name='ajax_carregar_cidades'),
    path('ajax/verificar-cidade-bd/', views.verificar_cidade_bd, name='verificar_cidade_bd'),
    path('ajax/verificar-cep/', views.verificar_cep, name='verificar_cep'),
]
