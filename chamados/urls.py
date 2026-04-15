from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_chamados, name='listar_chamados'),
    path('abrir/', views.abrir_chamado, name='abrir_chamado'),
    path('chamado/<int:pk>/', views.detalhar_chamado, name='detalhar_chamado'),
]