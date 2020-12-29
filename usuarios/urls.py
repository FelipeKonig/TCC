from django.urls import path
from .views import SignUpView, carregar_cidades

app_name = 'usuarios'

urlpatterns = [
    path('cadastro', SignUpView.as_view(), name='cadastrousuario'),
    path('ajax/carregar-cidades/', carregar_cidades, name='ajax_carregar_cidades'),
]
