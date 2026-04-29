from django.shortcuts import render, redirect, get_object_or_404
from .models import Chamado, Imovel, Prestador
from .forms import AbrirChamadoForm, AtualizarChamadoForm, ImovelForm, PrestadorForm

def listar_chamados(request):
    chamados = Chamado.objects.all().order_by('-data_abertura')
    return render(request, 'chamados/listar.html', {'chamados': chamados})

def abrir_chamado(request):
    if request.method == 'POST':
        form = AbrirChamadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_chamados')
    else:
        form = AbrirChamadoForm()
    return render(request, 'chamados/abrir.html', {'form': form})

def detalhar_chamado(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    return render(request, 'chamados/detalhar.html', {'chamado': chamado})

def atualizar_chamado(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == 'concluido':
        return redirect('detalhar_chamado', pk=chamado.pk)
    if request.method == 'POST':
        form = AtualizarChamadoForm(request.POST, request.FILES, instance=chamado)
        if form.is_valid():
            form.save()
            return redirect('detalhar_chamado', pk=chamado.pk)
    else:
        form = AtualizarChamadoForm(instance=chamado)
    return render(request, 'chamados/atualizar.html', {'form': form, 'chamado': chamado})

def encerrar_chamado(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == 'concluido':
        return redirect('detalhar_chamado', pk=chamado.pk)
    if request.method == 'POST':
        chamado.status = 'concluido'
        chamado.observacao = request.POST.get('observacao', '')
        chamado.save()
        return redirect('detalhar_chamado', pk=chamado.pk)
    return render(request, 'chamados/encerrar.html', {'chamado': chamado})

def listar_imoveis(request):
    imoveis = Imovel.objects.all()
    return render(request, 'chamados/imoveis/listar.html', {'imoveis': imoveis})

def cadastrar_imovel(request):
    if request.method == 'POST':
        form = ImovelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_imoveis')
    else:
        form = ImovelForm()
    return render(request, 'chamados/imoveis/cadastrar.html', {'form': form})

def listar_prestadores(request):
    prestadores = Prestador.objects.all()
    return render(request, 'chamados/prestadores/listar.html', {'prestadores': prestadores})

def cadastrar_prestador(request):
    if request.method == 'POST':
        form = PrestadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_prestadores')
    else:
        form = PrestadorForm()
    return render(request, 'chamados/prestadores/cadastrar.html', {'form': form})