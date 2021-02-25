from django.test import TestCase, Client
from django.urls import reverse

from ..models import *
from ...usuarios.models import CustomUsuario
from ...vitrines.models import Vitrine
from model_mommy import mommy

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.usuario = mommy.make(CustomUsuario)
        cls.vitrine = mommy.make(Vitrine, vendedor=cls.usuario, status=True)
        cls.categoria = mommy.make(Categoria, status=True)
        cls.produto = mommy.make(Produto, vitrine=cls.vitrine, categoria=cls.categoria, status=True)

    def test_criar_produto(self):

        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        response = cliente.get(reverse('produtos:criar_produto'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos/produto_cadastro.html')

        # para não dar erro no cadastro
        data = {
            'nome': 'aaaa',
            'preco': '1',
            'descricao': 'dfdsfds',
            'quantidade': '3',
            'categoria': 'fds|1'
        }
        url = reverse('produtos:criar_produto')
        response = cliente.post(url, data)
        self.assertEquals(response.status_code, 302)

        # para não dar erro no cadastro
        data = {
            'nome': 'aaaa',
            'preco': '1',
            'descricao': 'dfdsfds',
            'categoria': 'fds|1'
        }
        url = reverse('produtos:criar_produto')
        response = cliente.post(url, data)
        self.assertEquals(response.status_code, 200)

    def test_editar_produto(self):

        usuario = CustomUsuario.objects.get(id=self.usuario.pk)
        cliente = Client()
        login = cliente.force_login(usuario)

        # acessar a pagina para editar
        url = reverse('produtos:editar_produto')
        response = cliente.post(url, {'campoIDProduto': '1'})
        self.assertEquals(response.status_code, 200)

        # editando o produto
        data = {
            'campoIDProduto': '1',
            'nome': 'bbb',
            'preco': '1',
            'descricao': 'dfdsfds',
            'categoria': 'fds|1'
        }
        url = reverse('produtos:editar_produto')
        response = cliente.post(url, data)
        self.assertEquals(response.status_code, 302)
