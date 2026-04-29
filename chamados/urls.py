from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_chamados, name='listar_chamados'),
    path('abrir/', views.abrir_chamado, name='abrir_chamado'),
    path('chamado/<int:pk>/', views.detalhar_chamado, name='detalhar_chamado'),
    path('chamado/<int:pk>/atualizar/', views.atualizar_chamado, name='atualizar_chamado'),
    path('chamado/<int:pk>/encerrar/', views.encerrar_chamado, name='encerrar_chamado'),

    path('imoveis/', views.listar_imoveis, name='listar_imoveis'),
    path('imoveis/cadastrar/', views.cadastrar_imovel, name='cadastrar_imovel'),

    path('prestadores/', views.listar_prestadores, name='listar_prestadores'),
    path('prestadores/cadastrar/', views.cadastrar_prestador, name='cadastrar_prestador'),
]