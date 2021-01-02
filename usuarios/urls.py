from django.urls import path
from .views import SignUpView, CustomLoginView, carregar_cidades
from .forms import UsuarioLoginForm

app_name = 'usuarios'
from django.contrib.auth import views

urlpatterns = [
    path('cadastro', SignUpView.as_view(), name='cadastrousuario'),
    path('login', CustomLoginView.as_view(), name='login'),
    # path('ajax/carregar-cidades/', carregar_cidades, name='ajax_carregar_cidades'),
]
