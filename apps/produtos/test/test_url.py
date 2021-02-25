from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import *

class test_urls(SimpleTestCase):

    def test_produto_cadastro_url(self):
        url = reverse('produtos:criar_produto')
        self.assertEquals(resolve(url).func.view_class, CriarProduto)

    def test_produto_cadastro_url(self):
        url = reverse('produtos:deletar_produto')
        self.assertEquals(resolve(url).func, deletar_produto)

    def test_produto_cadastro_url(self):
        url = reverse('produtos:editar_produto')
        self.assertEquals(resolve(url).func, editar_produto)

    def test_produto_cadastro_url(self):
        url = reverse('produtos:visualizar_produto')
        self.assertEquals(resolve(url).func, visualizar_produto)

    #AJAX
    def test_ajax_carregar_subcategorias_url(self):
        url = reverse('produtos:ajax_carregar_subcategorias')
        self.assertEquals(resolve(url).func, carregar_subcategorias)
