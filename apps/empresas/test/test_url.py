from model_mommy import mommy
from django.test import TestCase

from ..models import Empresa

from ..views.empresa import *

from django.urls import reverse, resolve


class Test_Urls(TestCase):

    def setUp(self):
        self.empresa = mommy.make(Empresa)
        self.empresa.save()

    def test_cadastro_empresa(self):
        url = reverse('empresas:criar_empresa')
        self.assertEquals(resolve(url).func.view_class, CriarEmpresa)

    # def test_editar_empresa(self):
    #     empresa = Empresa.objects.get(id=self.empresa.id)
    #     url = reverse('empresas:editar_empresa', kwargs={'pk': empresa.id})
    #     self.assertEquals(resolve(url).func, editar_empresa)
    #
    # def test_deletar_empresa(self):
    #     empresa = Empresa.objects.get(id=self.empresa.id)
    #     url = reverse('empresas:deletar_empresa', kwargs={'pk': empresa.id})
    #     self.assertEquals(resolve(url).func, deletar_empresa)

    def test_listar_empresas(self):
        url = reverse('empresas:empresa_perfil')
        self.assertEquals(resolve(url).func, empresa_perfil)
