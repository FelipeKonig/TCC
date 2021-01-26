from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView
)

from apps.usuarios.models import CustomUsuario
from apps.vitrines.forms import CadastroVitrine
from apps.vitrines.models import Vitrine


def consulta_vitrine(usuario):
    query_set = Vitrine.objects.filter(vendedor=usuario, status=True)
    return query_set


@login_required(login_url='/usuarios/login')
def deletar_vitrine(request, pk):
    vitrine = get_object_or_404(Vitrine, id=pk)
    vitrine.status = False
    vitrine.save()
    messages.success(request, 'Vitrine deletada com sucesso!')
    return redirect('vitrines:minha_vitrine')


@login_required(login_url='/usuarios/login')
def listar_vitrine(request):
    usuario_logado = CustomUsuario.objects.get(email=request.user)

    query_set = consulta_vitrine(usuario_logado)

    if query_set is None:
        tamanho_resultado_query_set = 0
    else:
        tamanho_resultado_query_set = len(query_set)

    vitrine = Vitrine.objects.filter(vendedor=usuario_logado, status=True).first()
    print(query_set)
    context = {
        'usuario': usuario_logado,
        'vitrine': vitrine,
        'resultado_busca_vitrine': tamanho_resultado_query_set,

    }

    return render(request, 'vitrines/page-profile-seller.html', context)


class CriarVitrine(LoginRequiredMixin, CreateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        form = super().get_form(CadastroVitrine)

        query_set = consulta_vitrine(usuario_logado)
        print(query_set)
        if query_set is None:
            tamanho_resultado_query_set = 0
        else:
            tamanho_resultado_query_set = len(query_set)

        context = {
            'usuario': usuario_logado,
            'form': form,
            'resultado_busca_vitrine': tamanho_resultado_query_set
        }

        return render(request, 'vitrines/cadastros/vitrine_cadastro.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(CadastroVitrine)

        if form.is_valid():
            usuario_logado = CustomUsuario.objects.get(email=request.user)
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']
            vitrine = Vitrine.objects.create(nome=nome, descricao=descricao, vendedor=usuario_logado)
            vitrine.save()

            messages.success(request, 'Vitrine cadastrada com sucesso!')
            return redirect('vitrines:minha_vitrine')
        else:
            messages.error(request, 'Erro ao enviar formulário!')

        usuario_logado = CustomUsuario.objects.get(email=request.user)

        context = {
            'form': form,
            'usuario': usuario_logado
        }

        return render(request, 'vitrines/cadastros/vitrine_cadastro.html', context)


class EditarVitrine(LoginRequiredMixin, UpdateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        vitrine = get_object_or_404(Vitrine, pk=self.kwargs['pk'])
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        form = CadastroVitrine(instance=vitrine)

        print(vitrine)
        context = {
            'usuario': usuario_logado,
            'form': form
        }

        return render(request, 'vitrines/cadastros/vitrine_editar.html', context)

    def post(self, request, *args, **kwargs):
        vitrine = get_object_or_404(Vitrine, pk=self.kwargs['pk'])
        form = self.get_form(CadastroVitrine)
        usuario_logado = CustomUsuario.objects.get(email=request.user)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            descricao = form.cleaned_data['descricao']

            vitrine.nome = nome
            vitrine.descricao = descricao

            vitrine.save()
            messages.success(request, 'Vitrine editada com sucesso!')
            return redirect('vitrines:minha_vitrine')

        context = {
            'usuario': usuario_logado,
            'form': form
        }

        return render(request, 'vitrines/cadastros/vitrine_editar.html', context)
