from django.db import models

from mysite import settings


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=200, help_text='Obrigatório')


class SubCategoria(models.Model):
    nome = models.CharField('Nome', max_length=200, help_text='Não obrigatório')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, default="")


class Produto(models.Model):
    nome = models.CharField('Nome', max_length=250, help_text='Obrigatório')
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default="")
    descricao = models.CharField('Descrição', max_length=450)
    quantidade = models.IntegerField('Quantidade')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return '{}-{}-{}-{}-{}'.format(self.nome, self.preco, self.quantidade, self.descricao, self.vendedor)


class Caracteristica(models.Model):
    topico = models.CharField('Tópico', max_length=200)
    descricao = models.CharField('Descrição', max_length=450)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default="")

    class Meta:
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'

    def __str__(self):
        return '{}-{}-{}'.format(self.topico, self.descricao, self.produto)