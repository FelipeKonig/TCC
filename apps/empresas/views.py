from django.shortcuts import render
from django.views.generic import CreateView
from .forms import CadastroEmpresa


class CriarEmpresa(CreateView):

    def get(self, request, *args, **kwargs):
        form = super().get_form(CadastroEmpresa)
        context = {
            'form': form
        }
        return render(request, 'empresas/empresa_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(CadastroEmpresa)
        context = {
            'form': form
        }
        return render(request, 'empresas/empresa_cadastro.html', context)

