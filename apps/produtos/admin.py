from django.contrib import admin

from .models import Categoria, SubCategoria, Produto, Caracteristica

admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Produto)
admin.site.register(Caracteristica)
