from django.contrib import admin

from .models import Pedido, Pedido_Produto
# Register your models here.
admin.site.register(Pedido)
admin.site.register(Pedido_Produto)
