from django import forms
from .models import Chamado, Imovel, Prestador

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