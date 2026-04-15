from django.shortcuts import render, redirect, get_object_or_404
from .models import Chamado
from .forms import ChamadoForm

def listar_chamados(request):
    chamados = Chamado.objects.all().order_by('-data_abertura')
    return render(request, 'chamados/listar.html', {'chamados': chamados})

def abrir_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_chamados')
    else:
        form = ChamadoForm()
    return render(request, 'chamados/abrir.html', {'form': form})

def detalhar_chamado(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    return render(request, 'chamados/detalhar.html', {'chamado': chamado})