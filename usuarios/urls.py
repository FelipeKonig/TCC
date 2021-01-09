from django.urls import path
from .views import (
    SignUp,
    LoginCustomizado,
    ResetarSenha,
    MensagemResetarSenhaEmail
)

app_name = 'usuarios'

urlpatterns = [
    path('cadastro', SignUp.as_view(), name='cadastrousuario'),
    path('login', LoginCustomizado.as_view(), name='login'),
    path('resetar-senha', ResetarSenha.as_view(), name='resetarsenha'),
    path('resetar-senha-sucesso', MensagemResetarSenhaEmail.as_view(), name='sucessoresetarsenha')
    # path('ajax/carregar-cidades/', carregar_cidades, name='ajax_carregar_cidades'),
]
