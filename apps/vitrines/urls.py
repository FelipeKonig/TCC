from django.conf.urls import url
from django.urls import path

from apps.vitrines.views import (
    CriarVitrine,
    listar_vitrine,
    deletar_vitrine,
    EditarVitrine
)

app_name = 'vitrines'

urlpatterns = [
    path('criar-vitrine/', CriarVitrine.as_view(), name='criar_vitrine'),
    path('minha-vitrine/', listar_vitrine, name='minha_vitrine'),
    path('editar-vitrine/<int:pk>', EditarVitrine.as_view(), name='editar_vitrine'),
    path('deletar-vitrine/<int:pk>', deletar_vitrine, name='deletar_vitrine')
   # url(r'^editar-vitrine/$', EditarVitrine.as_view(), name='editar_vitrine'),


]
