from django.urls import path

from .views import (
    SignUp,
    LoginCustomizado,
    EmailTokenSenha,
    MensagemResetarSenhaEmail,
    ResetarSenha,
    ResetarSenhaMensagemCompleta,
    AlteracaoSenha,
<<<<<<< HEAD:apps/usuarios/urls.py
    CriarPefilUsuario
=======
    SignUpView,
    CustomLoginView
>>>>>>> dda3065af2350bb402bb1ef1d4c1773066c3986e:usuarios/urls.py
)
from .forms import UsuarioLoginForm

app_name = 'usuarios'

from . import views

urlpatterns = [
    path('cadastro', SignUp.as_view(), name='cadastrousuario'),
    path('login', LoginCustomizado.as_view(), name='login'),
    path('resetar-senha', EmailTokenSenha.as_view(), name='resetarsenha'),
    path('resetar-senha-sucesso-email', MensagemResetarSenhaEmail.as_view(), name='sucessoresetarsenha'),
    path('reset/<uidb64>/<token>', ResetarSenha.as_view(), name='novasenha'),
    path('redifinicao-completa', ResetarSenhaMensagemCompleta.as_view(), name='redifinicaocompleta'),
    path('alterar-senha', AlteracaoSenha.as_view(), name='alterarsenha'),
<<<<<<< HEAD:apps/usuarios/urls.py
    path('criar-perfil', CriarPefilUsuario.as_view(), name='criarperfil')
=======
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
>>>>>>> dda3065af2350bb402bb1ef1d4c1773066c3986e:usuarios/urls.py
]
