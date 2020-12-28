from django.urls import path
from .views import SignUpView

app_name = 'usuarios'

urlpatterns = [
    path('cadastro', SignUpView.as_view(), name='cadastrousuario'),
]
