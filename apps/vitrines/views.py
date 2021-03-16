from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import (
    CreateView,
)

from apps.produtos.models import Produto, ImagemProduto
from apps.usuarios.models import CustomUsuario
from apps.vitrines.forms import CadastroVitrine
from apps.vitrines.models import Vitrine

recuperar_id_editar_vitrine = {}
recuperar_id_deletar_vitrine = {}


def consulta_vitrine(usuario):
    query_set = Vitrine.objects.filter(vendedor=usuario, status=True)
    return query_set


@login_required(login_url='/usuarios/login')
def deletar_vitrine(request):
    if len(request.POST) == 2:
        vitrine = get_object_or_404(Vitrine, pk=request.POST.get('id'))
        recuperar_id_deletar_vitrine['vitrine'] = vitrine
        vitrine.status = False
        vitrine.save()

    if not recuperar_id_deletar_vitrine['vitrine'].status:
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
    produtos = Produto.objects.filter(vitrine=vitrine, status=True)
    imagens_produtos = ImagemProduto.objects.filter(produto__in=produtos)

    #No resultado query_set verifico se já existe uma vitrine ou não, caso ele já existe,
    #redireciono e mostro os dados da vitrine, caso contrário o usuário deverá cadastrar a sua vitrine
    context = {
        'usuario': usuario_logado,
        'vitrine': vitrine,
        'resultado_busca_vitrine': tamanho_resultado_query_set,
        'produtos': produtos,
        'imagens_produtos': imagens_produtos
    }

    return render(request, 'vitrines/vitrine_listar.html', context)


class CriarVitrine(LoginRequiredMixin, CreateView):
    login_url = '/usuarios/login'

    def get(self, request, *args, **kwargs):
        usuario_logado = CustomUsuario.objects.get(email=request.user)
        form = super().get_form(CadastroVitrine)

        query_set = consulta_vitrine(usuario_logado)
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

            try:
                if request.POST['empresa']:
                    vitrine.empresa = request.user.empresa
            except:
                vitrine.empresa = None

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


def editar_vitrine(request):
    if len(request.POST) == 2:
        if not recuperar_id_editar_vitrine:
            recuperar_id_editar_vitrine['id'] = request.POST.get('id')

    vitrine = retornar_vitrine()
    if str(request.method) == 'POST':
        if len(request.POST) > 2:
            form = CadastroVitrine(request.POST, instance=vitrine)

            if form.is_valid():
                nome = form.cleaned_data['nome']
                descricao = form.cleaned_data['descricao']

                vitrine.nome = nome
                vitrine.descricao = descricao

                try:
                    if request.POST['empresa']:
                        vitrine.empresa = request.user.empresa
                except:
                    vitrine.empresa = None

                vitrine.save()
                messages.success(request, 'Vitrine editada com sucesso!')
                return redirect('vitrines:minha_vitrine')
            else:
                messages.error(request, 'Erro ao enviar formulário!')

    form = CadastroVitrine(instance=vitrine)
    usuario_logado = CustomUsuario.objects.get(email=request.user)

    context = {
        'form': form,
        'usuario': usuario_logado,
        'vitrine': vitrine
    }

    return render(request, 'vitrines/cadastros/vitrine_editar.html', context)


def retornar_vitrine():
    if recuperar_id_editar_vitrine:
        vitrine = get_object_or_404(Vitrine, pk=recuperar_id_editar_vitrine['id'])
        return vitrine
