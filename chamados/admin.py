from django.contrib import admin
from .models import Imovel, Chamado, Prestador

admin.site.register(Imovel)
admin.site.register(Chamado)
admin.site.register(Prestador)