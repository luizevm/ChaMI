from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Chamados
    path('', views.listar_chamados, name='listar_chamados'),
    path('abrir/', views.abrir_chamado, name='abrir_chamado'),
    path('chamado/<int:pk>/', views.detalhar_chamado, name='detalhar_chamado'),
    path('chamado/<int:pk>/atualizar/', views.atualizar_chamado, name='atualizar_chamado'),
    path('chamado/<int:pk>/encerrar/', views.encerrar_chamado, name='encerrar_chamado'),
    path('chamado/<int:pk>/cancelar/', views.cancelar_chamado, name='cancelar_chamado'),
    path('chamado/<int:pk>/orcamento/', views.enviar_orcamento, name='enviar_orcamento'),
    path('chamado/<int:pk>/em-andamento/', views.marcar_em_andamento, name='marcar_em_andamento'),
    path('chamado/<int:pk>/aprovar-orcamento/', views.aprovar_orcamento, name='aprovar_orcamento'),
    path('chamado/<int:pk>/reprovar-orcamento/', views.reprovar_orcamento, name='reprovar_orcamento'),
    path('chamado/<int:pk>/resolver-internamente/', views.resolver_internamente, name='resolver_internamente'),

    # Imóveis
    path('imoveis/', views.listar_imoveis, name='listar_imoveis'),
    path('imoveis/cadastrar/', views.cadastrar_imovel, name='cadastrar_imovel'),
    path('imoveis/<int:pk>/editar/', views.editar_imovel, name='editar_imovel'),
    path('imoveis/<int:pk>/excluir/', views.excluir_imovel, name='excluir_imovel'),

    # Prestadores
    path('prestadores/', views.listar_prestadores, name='listar_prestadores'),
    path('prestadores/cadastrar/', views.cadastrar_prestador, name='cadastrar_prestador'),
    path('prestadores/cadastrar-usuario/', views.cadastrar_prestador_user, name='cadastrar_prestador_user'),
    path('prestadores/<int:pk>/editar/', views.editar_prestador, name='editar_prestador'),
    path('prestadores/<int:pk>/excluir/', views.excluir_prestador, name='excluir_prestador'),

    # Inquilinos
    path('inquilinos/', views.listar_inquilinos, name='listar_inquilinos'),
    path('inquilinos/cadastrar/', views.cadastrar_inquilino, name='cadastrar_inquilino'),
]