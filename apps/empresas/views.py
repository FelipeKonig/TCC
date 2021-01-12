from django.shortcuts import render
from django.views.generic import CreateView
from .forms import CadastroEmpresa


class CriarEmpresa(CreateView):
    form_class = CadastroEmpresa
    template_name = 'empresas/empresa_cadastro.html'

