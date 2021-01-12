from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CustomUsuario)
admin.site.register(Endereco)
admin.site.register(Telefone)
admin.site.register(Estado)
admin.site.register(Cidade)
