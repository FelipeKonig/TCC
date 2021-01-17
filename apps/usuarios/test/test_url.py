from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views.usuario import *
from ..views.endereco import *


from TCC.usuarios.views import definir_endereco_padrao


class test_urls(SimpleTestCase):

    # testando todas as urls verificando pela função da view
    # se quiser pode fazer o teste verificando outras coisas

    def test_usuario_cadastro_url(self):
        url = reverse('usuarios:cadastrousuario')
        # caso queira ver as informações que cada url está recebendo
        # print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, SignUp)

    def test_usuario_cadastro_url(self):
        url = reverse('usuarios:login')
        self.assertEquals(resolve(url).func.view_class, LoginCustomizado)

    def test_perfil_usuario_url(self):
        url = reverse('usuarios:perfil_principal')
        self.assertEquals(resolve(url).func, perfil_principal)

    def test_adicionar_endereco_url(self):
        url = reverse('usuarios:perfil_endereco_adicionar')
        self.assertEquals(resolve(url).func, adicionar_endereco)

    def test_editar_endereco_url(self):
        url = reverse('usuarios:editar_endereco')
        self.assertEquals(resolve(url).func, editar_endereco)

    def test_deletar_endereco_url(self):
        url = reverse('usuarios:deletar_endereco')
        self.assertEquals(resolve(url).func, deletar_endereco)

    def test_definir_endereco_padrao_url(self):
        url = reverse('usuarios:definir_endereco_padrao')
        self.assertEquals(resolve(url).func, definir_endereco_padrao)

    # AJAX
    def test_verificar_cidade_bd_url(self):
        url = reverse('usuarios:verificar_cidade_bd')
        self.assertEquals(resolve(url).func, verificar_cidade_bd)

    # AJAX
    def test_verificar_cep_url(self):
        url = reverse('usuarios:verificar_cep')
        self.assertEquals(resolve(url).func, verificar_cep)
