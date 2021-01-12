from django.urls import path

from . import views

app_name = 'e-commerce'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('perfil/', views.perfil_principal, name='perfil_principal'),
]
