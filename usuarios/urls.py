from django.urls import path
from .views import (
    SignUp,
    LoginCustomizado,
    EmailTokenSenha,
    MensagemResetarSenhaEmail,
    ResetarSenha,
    ResetarSenhaMensagemCompleta,
    AlteracaoSenha,
    CriarPefilUsuario
)

app_name = 'usuarios'

urlpatterns = [
    path('cadastro', SignUp.as_view(), name='cadastrousuario'),
    path('login', LoginCustomizado.as_view(), name='login'),
    path('resetar-senha', EmailTokenSenha.as_view(), name='resetarsenha'),
    path('resetar-senha-sucesso-email', MensagemResetarSenhaEmail.as_view(), name='sucessoresetarsenha'),
    path('reset/<uidb64>/<token>', ResetarSenha.as_view(), name='novasenha'),
    path('redifinicao-completa', ResetarSenhaMensagemCompleta.as_view(), name='redifinicaocompleta'),
    path('alterar-senha', AlteracaoSenha.as_view(), name='alterarsenha'),
    path('criar-perfil', CriarPefilUsuario.as_view(), name='criarperfil')
]
