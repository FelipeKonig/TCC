from django.urls import path
from .views import SignUpView, CustomLoginView
from .forms import UsuarioLoginForm

app_name = 'usuarios'
from django.contrib.auth import views

from . import views

urlpatterns = [
    path('cadastro', SignUpView.as_view(), name='cadastrousuario'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('perfil/', views.perfil_principal, name='perfil_principal'),
    path('perfil/endereco', views.perfil_endereco, name='perfil_endereco'),
    path('perfil/endereco/adicionar', views.adicionar_endereco, name='perfil_endereco_adicionar'),
    path('perfil/endereco/editar', views.editar_endereco, name='editar_endereco'),
    path('perfil/endereco/deletar', views.deletar_endereco, name='deletar_endereco'),
    path('perfil/endereco/definir-endereco-padrao', views.definir_endereco_padrao, name='definir_endereco_padrao'),
    path('ajax/carregar-cidades/', views.carregar_cidades, name='ajax_carregar_cidades'),
    path('ajax/verificar-cidade-bd/', views.verificar_cidade_bd, name='verificar_cidade_bd'),
    path('ajax/verificar-cep/', views.verificar_cep, name='verificar_cep'),
]
