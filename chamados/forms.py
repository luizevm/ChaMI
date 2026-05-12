from django import forms
from .models import Chamado, Imovel, Prestador
from django.contrib.auth.models import User

class AbrirChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['imovel', 'descricao', 'categoria']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class AtualizarChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['imovel', 'descricao', 'categoria', 'status', 'prestador', 'orcamento', 'valor_final', 'observacao', 'anexo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['endereco', 'complemento', 'inquilino', 'telefone']

class PrestadorForm(forms.ModelForm):
    class Meta:
        model = Prestador
        fields = ['nome', 'telefone', 'area']

class InquilinoForm(forms.Form):
    nome = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11, help_text='Somente números')
    senha = forms.CharField(widget=forms.PasswordInput)
    imovel = forms.ModelChoiceField(queryset=Imovel.objects.all())
    
class PrestadorUserForm(forms.Form):
    nome = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11, help_text='Somente números')
    senha = forms.CharField(widget=forms.PasswordInput)
    prestador = forms.ModelChoiceField(queryset=Prestador.objects.all())
    
class OrcamentoForm(forms.Form):
    orcamento = forms.DecimalField(max_digits=10, decimal_places=2, label='Valor do Orçamento (R$)')
    observacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Descrição do serviço')