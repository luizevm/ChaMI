from django import forms
from .models import Chamado

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['imovel', 'descricao', 'categoria']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }