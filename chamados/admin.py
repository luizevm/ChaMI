from django.contrib import admin
from .models import Imovel, Chamado, Prestador, Perfil

admin.site.register(Imovel)
admin.site.register(Chamado)
admin.site.register(Prestador)
admin.site.register(Perfil)