from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Chamado, Imovel, Prestador, Perfil
from .forms import AbrirChamadoForm, AtualizarChamadoForm, ImovelForm, PrestadorForm, InquilinoForm, PrestadorUserForm, OrcamentoForm
from django.contrib.auth.models import User

@login_required
def listar_chamados(request):
    if request.user.is_superuser:
        chamados = Chamado.objects.all().order_by('-data_abertura')
    else:
        try:
            perfil = Perfil.objects.get(user=request.user)
            if perfil.tipo == 'admin':
                chamados = Chamado.objects.all().order_by('-data_abertura')
            elif perfil.tipo == 'inquilino':
                chamados = Chamado.objects.filter(imovel=perfil.imovel).order_by('-data_abertura')
            elif perfil.tipo == 'prestador':
                chamados = Chamado.objects.filter(prestador=perfil.prestador).order_by('-data_abertura')
            else:
                chamados = Chamado.objects.none()
        except Perfil.DoesNotExist:
            chamados = Chamado.objects.none()

    return render(request, 'chamados/listar.html', {'chamados': chamados})

@login_required
def abrir_chamado(request):
    if request.method == 'POST':
        form = AbrirChamadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_chamados')
    else:
        form = AbrirChamadoForm()
        if not request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(user=request.user)
                if perfil.tipo == 'inquilino':
                    form.fields['imovel'].initial = perfil.imovel
                    form.fields['imovel'].disabled = True
            except Perfil.DoesNotExist:
                pass
    return render(request, 'chamados/abrir.html', {'form': form})

@login_required
def detalhar_chamado(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    try:
        perfil = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        perfil = None
    return render(request, 'chamados/detalhar.html', {'chamado': chamado, 'perfil': perfil})

@login_required
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

@login_required
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

@login_required
def listar_imoveis(request):
    imoveis = Imovel.objects.all()
    return render(request, 'chamados/imoveis/listar.html', {'imoveis': imoveis})

@login_required
def cadastrar_imovel(request):
    if request.method == 'POST':
        form = ImovelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_imoveis')
    else:
        form = ImovelForm()
    return render(request, 'chamados/imoveis/cadastrar.html', {'form': form})

@login_required
def listar_prestadores(request):
    prestadores = Prestador.objects.all()
    return render(request, 'chamados/prestadores/listar.html', {'prestadores': prestadores})

@login_required
def cadastrar_prestador(request):
    if request.method == 'POST':
        form = PrestadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_prestadores')
    else:
        form = PrestadorForm()
    return render(request, 'chamados/prestadores/cadastrar.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('listar_chamados')
            try:
                perfil = Perfil.objects.get(user=user)
                if perfil.tipo == 'admin':
                    return redirect('listar_chamados')
                elif perfil.tipo == 'inquilino':
                    return redirect('listar_chamados')
                elif perfil.tipo == 'prestador':
                    return redirect('listar_chamados')
            except Perfil.DoesNotExist:
                return render(request, 'chamados/login.html', {'erro': 'Perfil não encontrado. Contate o administrador.'})
        else:
            return render(request, 'chamados/login.html', {'erro': 'Usuário ou senha incorretos.'})
    return render(request, 'chamados/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def cadastrar_inquilino(request):
    if request.method == 'POST':
        form = InquilinoForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            nome = form.cleaned_data['nome']
            senha = form.cleaned_data['senha']
            imovel = form.cleaned_data['imovel']

            user = User.objects.create_user(
                username=cpf,
                password=senha,
                first_name=nome
            )

            Perfil.objects.create(
                user=user,
                tipo='inquilino',
                imovel=imovel
            )

            return redirect('listar_inquilinos')
    else:
        form = InquilinoForm()
    return render(request, 'chamados/inquilinos/cadastrar.html', {'form': form})

@login_required
def listar_inquilinos(request):
    inquilinos = Perfil.objects.filter(tipo='inquilino')
    return render(request, 'chamados/inquilinos/listar.html', {'inquilinos': inquilinos})

@login_required
def cancelar_chamado(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    perfil = Perfil.objects.get(user=request.user)
    
    if perfil.tipo == 'inquilino' and chamado.status != 'aberto':
        return redirect('detalhar_chamado', pk=chamado.pk)
    
    if request.method == 'POST':
        chamado.status = 'cancelado'
        chamado.save()
        return redirect('listar_chamados')
    
    return render(request, 'chamados/cancelar.html', {'chamado': chamado})

@login_required
def cadastrar_prestador_user(request):
    if request.method == 'POST':
        form = PrestadorUserForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            nome = form.cleaned_data['nome']
            senha = form.cleaned_data['senha']
            prestador = form.cleaned_data['prestador']

            user = User.objects.create_user(
                username=cpf,
                password=senha,
                first_name=nome
            )

            Perfil.objects.create(
                user=user,
                tipo='prestador',
                prestador=prestador
            )

            return redirect('listar_prestadores')
    else:
        form = PrestadorUserForm()
    return render(request, 'chamados/prestadores/cadastrar_user.html', {'form': form})

@login_required
def enviar_orcamento(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            chamado.orcamento = form.cleaned_data['orcamento']
            chamado.observacao = form.cleaned_data['observacao']
            chamado.status = 'orcamento_enviado'
            chamado.save()
            return redirect('listar_chamados')
    else:
        form = OrcamentoForm()
    return render(request, 'chamados/orcamento.html', {'form': form, 'chamado': chamado})

@login_required
def marcar_em_andamento(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == 'orcamento_aprovado':
        chamado.status = 'em_andamento'
        chamado.save()
    return redirect('detalhar_chamado', pk=chamado.pk)

@login_required
def aprovar_orcamento(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == 'orcamento_enviado':
        chamado.status = 'orcamento_aprovado'
        chamado.save()
    return redirect('detalhar_chamado', pk=chamado.pk)

@login_required
def reprovar_orcamento(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == 'orcamento_enviado':
        chamado.status = 'orcamento_reprovado'
        chamado.save()
    return redirect('detalhar_chamado', pk=chamado.pk)

@login_required
def resolver_internamente(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if request.method == 'POST':
        chamado.status = 'resolvido_internamente'
        chamado.observacao = request.POST.get('observacao', '')
        chamado.save()
        return redirect('detalhar_chamado', pk=chamado.pk)
    return render(request, 'chamados/resolver_internamente.html', {'chamado': chamado})

@login_required
def editar_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    if request.method == 'POST':
        form = ImovelForm(request.POST, instance=imovel)
        if form.is_valid():
            form.save()
            return redirect('listar_imoveis')
    else:
        form = ImovelForm(instance=imovel)
    return render(request, 'chamados/imoveis/editar.html', {'form': form, 'imovel': imovel})

@login_required
def excluir_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    if request.method == 'POST':
        imovel.delete()
        return redirect('listar_imoveis')
    return render(request, 'chamados/imoveis/excluir.html', {'imovel': imovel})

@login_required
def editar_prestador(request, pk):
    prestador = get_object_or_404(Prestador, pk=pk)
    if request.method == 'POST':
        form = PrestadorForm(request.POST, instance=prestador)
        if form.is_valid():
            form.save()
            return redirect('listar_prestadores')
    else:
        form = PrestadorForm(instance=prestador)
    return render(request, 'chamados/prestadores/editar.html', {'form': form, 'prestador': prestador})

@login_required
def excluir_prestador(request, pk):
    prestador = get_object_or_404(Prestador, pk=pk)
    if request.method == 'POST':
        prestador.delete()
        return redirect('listar_prestadores')
    return render(request, 'chamados/prestadores/excluir.html', {'prestador': prestador})