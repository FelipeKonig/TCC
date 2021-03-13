from django.db import models

from apps.usuarios.models import CustomUsuario
from apps.produtos.models import Produto
from apps.vitrines.models import Vitrine
# Create your models here.

class Pedido(models.Model):
    cliente = models.ForeignKey(CustomUsuario, on_delete=models.PROTECT, default="")
    produto = models.ManyToManyField(Produto, through="Pedido_Produto")
    statusReservado = models.BooleanField('Reservado', default=False)
    statusFinalizado = models.BooleanField('Finalizado', default=False)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'pedido id: {}; cliente: {}; status de reserva: {}; status de entrega: {}'.format(
            self.pk,
            self.cliente.email,
            self.statusReservado,
            self.statusFinalizado
        )

class Pedido_Produto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vitrine, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField('Quantidade')
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2, help_text='Obrigatório')
    precoTotal = models.DecimalField('Preço total', max_digits=10, decimal_places=2, help_text='Obrigatório', default=0)
    dataCriacao = models.DateField('Data de criação')
    dataRetirada = models.DateField('Data de entrega', null=True)
    statusReservado = models.BooleanField('Reservado', default=False)
    statusFinalizado = models.BooleanField('Finalizado', default=False)

    class Meta:
        verbose_name = 'Pedido_Produto'
        verbose_name_plural = 'Pedidos_Produtos'

    def __str__(self):
        return 'pedido id: {}; produto: {}; vendedor: {}; status de reserva: {}; status de entrega: {}'.format(
            self.pedido.pk,
            self.produto.nome,
            self.vendedor.nome,
            self.statusReservado,
            self.statusFinalizado
        )
