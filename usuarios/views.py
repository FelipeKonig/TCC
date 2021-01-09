# a biblioteca requests é o padrão para fazer solicitações HTTP em Python
# utilizada no nosso caso para fazer a requisição da api do ibge
# obs: é necessário baixar ela no django, necessário baixar arquivos do requirements
import requests
import logging

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from .forms import (
    CustomUsuarioCreationForm,
    UsuarioLoginForm

)
from .models import (
    CustomUsuario,
    Cidade,
    Estado,
    Telefone, Endereco
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

logger = logging.getLogger(__name__)

class SignUpView(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('usuarios:cadastrousuario')
    form_class = CustomUsuarioCreationForm
    template_name = 'cadastros/usuario_cadastro.html'
    success_message = 'Cadastro realizado com sucesso'


class CustomLoginView(LoginView, SuccessMessageMixin):
    authentication_form = UsuarioLoginForm
    template_name = 'registration/login.html'
    success_message = 'Login realizado com sucesso'

@login_required
def perfil_principal(request):
    enderecos = Endereco.objects.filter(usuario=request.user)
    return render(request, 'usuarios/perfil-principal.html', {'enderecos':enderecos})

@login_required
def perfil_endereco(request):
    enderecos = Endereco.objects.filter(usuario=request.user)
    return render(request, 'usuarios/perfil-endereco.html', {'enderecos':enderecos})

@login_required
def endereco_formulario_adicionar(request):

    # busca na api do ibge os estados por ordem de nome
    # obs:Você pode copiar e colar o link no navegador para ver o arquivo Json gerado
    estados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome'

    # indica que quero obter os dados dessa requisição através do método .get()
    requisicao_estados = requests.get(estados)

    try:
        # indica que quero desserializar, no caso,
        # transformar as informações str para um dicionário através do método .json()
        lista = requisicao_estados.json()
    except ValueError:
        logger.critical("Não encontrou os estados")

    dicionario = {}

    # enumerate é usado em loops for ou ser convertido em uma lista de tuplas usando o método list()
    # ou seja, através do enumerate cria tuplas dos estados de acordo com o indice
    # se olhar o arquivo completo acessando o link acima fica mais fácil de entender o motivo
    for indice, estados in enumerate(lista):
        # adiciona as tuplas com os estados
        dicionario[indice] = estados

    return render(request, 'usuarios/perfil-endereco-formulario.html',{ 'estados': dicionario })

# AJAX
def carregar_cidades(request):

    sigla = request.GET.get('estado').split()[-1]
    logger.debug('sigla: {}'.format(sigla))

    cidades = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios'.format(sigla)
    requisicao_cidades = requests.get(cidades)

    try:
        lista = requisicao_cidades.json()
    except ValueError:
        logger.critical("Não encontrou as cidades")

    dicionario = {}
    for indice, cidades in enumerate(lista):

        # apenas filtrando os dados do objeto em cidades para pegar apenas o nome
        dicionario[indice] = cidades.get('nome')

    if request.is_ajax():
        return JsonResponse({'cidades': dicionario})
