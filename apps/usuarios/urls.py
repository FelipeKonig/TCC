from django.urls import path

from .views import usuario
from .views import endereco

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('cadastro', usuario.SignUp.as_view(), name='cadastrousuario'),
    path('login', usuario.LoginCustomizado.as_view(), name='login'),
    path('resetar-senha', usuario.EmailTokenSenha.as_view(), name='resetarsenha'),
    path('resetar-senha-sucesso-email', usuario.MensagemResetarSenhaEmail.as_view(), name='sucessoresetarsenha'),
    path('reset/<uidb64>/<token>', usuario.ResetarSenha.as_view(), name='novasenha'),
    path('redifinicao-completa', usuario.ResetarSenhaMensagemCompleta.as_view(), name='redifinicaocompleta'),
    path('alterar-senha', usuario.AlteracaoSenha.as_view(), name='alterarsenha'),
    path('criar-perfil', usuario.CriarPerfilUsuario.as_view(), name='criarperfil'),
    path('perfil', usuario.perfil_principal, name='perfil_principal'),
    path('perfil/configuracao', usuario.perfil_configuracao, name='perfil_configuracao'),
    path('perfil/endereco', endereco.perfil_endereco, name='perfil_endereco'),
    path('perfil/endereco/adicionar', endereco.adicionar_endereco, name='perfil_endereco_adicionar'),
    path('perfil/endereco/editar', endereco.editar_endereco, name='editar_endereco'),
    path('perfil/endereco/deletar', endereco.deletar_endereco, name='deletar_endereco'),
    path('perfil/endereco/definir-endereco-padrao', endereco.definir_endereco_padrao, name='definir_endereco_padrao'),
    path('ajax/carregar-cidades/', endereco.carregar_cidades, name='ajax_carregar_cidades'),
    path('ajax/verificar-cep/', endereco.verificar_cep, name='verificar_cep'),
]
