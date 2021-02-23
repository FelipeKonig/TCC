import os
import logging

from uuid import uuid4
from django.db import models
from stdimage import StdImageField
from mysite import settings

logger = logging.getLogger(__name__)

def adicionar_imagem_logo(instance, filename):

    buscar_produto = ImagemProduto.objects.filter(produto=instance.produto.pk)

    # criar novo arquivo caso o produto não ter nenhuma pasta propria
    if len(buscar_produto) == 0 :
        nome_arquivo = '{}'.format(uuid4().hex)
        # como a pasta já é preenchida com numeros aleatórios, manter o nome da imagem
        return os.path.join('fotoProduto/{}'.format(nome_arquivo), filename)
    else:
        nome_arquivo = str(buscar_produto[0].imagem).split('/')[1]

        # se o produto já tem sua propria pasta, adicionar imagem nela
        if os.path.exists('media/fotoProduto/{}'.format(nome_arquivo)):
            try:
                return os.path.join('fotoProduto/{}'.format(nome_arquivo), filename)
            # caso ela não ser encontrada, criar nova pasta para o produto
            except:
                return os.path.join('fotoProduto/{}'.format(nome_arquivo), filename)

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=200, help_text='Obrigatório')
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return '{}'.format(self.nome)


class SubCategoria(models.Model):
    nome = models.CharField('Nome', max_length=200, help_text='Não obrigatório')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, default="")
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'

    def __str__(self):
        return '{} - {}'.format(self.nome, self.categoria)

class Produto(models.Model):
    nome = models.CharField('Nome', max_length=250, help_text='Obrigatório')
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2, help_text='Obrigatório')
    descricao = models.CharField('Descrição', max_length=450, help_text='Obrigatório')
    quantidade = models.IntegerField('Quantidade', help_text='Obrigatório')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default='')
    subCategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, null=True)
    vitrine = models.ForeignKey('vitrines.Vitrine', on_delete=models.CASCADE, default='')
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return 'produto:{}; valor:{};quantidade:{}-{}'.format(self.nome, self.preco, self.quantidade, self.vitrine.vendedor)

class ImagemProduto(models.Model):
    imagem = StdImageField('Imagem do produto', upload_to=adicionar_imagem_logo, help_text='Obrigatório')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default='')
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Imagem do produto'
        verbose_name_plural = 'Imagens dos produtos'

    def __str__(self):
        return 'imagem:{}; status:{} -Produto:{}'.format(self.imagem, self.status, self.produto.nome)

    def nome_arquivo(self):
        nome_arquivo = str(self.imagem).split('/')[2]
        return nome_arquivo


class Caracteristica(models.Model):
    topico = models.CharField('Tópico', max_length=200)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default="")
    status = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'

    def __str__(self):
        return '{}; status:{}-produto:{}'.format(self.topico, self.status, self.produto.nome)

class Atributo(models.Model):
    caracteristica = models.ForeignKey(Caracteristica, on_delete=models.CASCADE, default="")
    nome = models.CharField('Nome', max_length=200)
    descricao = models.CharField('Descrição', max_length=450)

    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    def __str__(self):
        return '{}-caracteristica:{}'.format(self.nome, self.caracteristica)
