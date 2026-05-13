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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class AtualizarChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['imovel', 'descricao', 'categoria', 'status', 'prestador', 'orcamento', 'valor_final', 'observacao', 'anexo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['endereco', 'complemento', 'tipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PrestadorForm(forms.ModelForm):
    class Meta:
        model = Prestador
        fields = ['nome', 'telefone', 'area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class InquilinoForm(forms.Form):
    nome = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11, help_text='Somente números')
    senha = forms.CharField(widget=forms.PasswordInput)
    telefone = forms.CharField(max_length=20)
    imovel = forms.ModelChoiceField(
        queryset=Imovel.objects.filter(
            perfil__isnull=True
        ) | Imovel.objects.filter(
            perfil__tipo__in=['admin', 'prestador']
        ),
        label='Imóvel disponível'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        imoveis_disponiveis = Imovel.objects.exclude(
            perfil__tipo='inquilino'
        )
        self.fields['imovel'].queryset = imoveis_disponiveis
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if User.objects.filter(username=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado no sistema.')
        return cpf

class PrestadorUserForm(forms.Form):
    nome = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11, help_text='Somente números')
    senha = forms.CharField(widget=forms.PasswordInput)
    prestador = forms.ModelChoiceField(queryset=Prestador.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if User.objects.filter(username=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado no sistema.')
        return cpf

class OrcamentoForm(forms.Form):
    orcamento = forms.DecimalField(max_digits=10, decimal_places=2, label='Valor do Orçamento (R$)')
    observacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Descrição do serviço')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class AdminForm(forms.Form):
    nome = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11, help_text='Somente números')
    senha = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if User.objects.filter(username=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado no sistema.')
        return cpf

class EditarInquilinoForm(forms.Form):
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=20)
    imovel = forms.ModelChoiceField(
        queryset=Imovel.objects.none(),
        label='Imóvel'
    )
    nova_senha = forms.CharField(widget=forms.PasswordInput, required=False, help_text='Deixe em branco para não alterar')

    def __init__(self, *args, inquilino=None, **kwargs):
        super().__init__(*args, **kwargs)
        if inquilino:
            imoveis_disponiveis = Imovel.objects.exclude(
                perfil__tipo='inquilino'
            ) | Imovel.objects.filter(pk=inquilino.imovel.pk) if inquilino.imovel else Imovel.objects.exclude(
                perfil__tipo='inquilino'
            )
            self.fields['imovel'].queryset = imoveis_disponiveis
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class EditarAdminForm(forms.Form):
    nome = forms.CharField(max_length=100)
    nova_senha = forms.CharField(widget=forms.PasswordInput, required=False, help_text='Deixe em branco para não alterar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class EditarPrestadorUserForm(forms.Form):
    nome = forms.CharField(max_length=100)
    prestador = forms.ModelChoiceField(queryset=Prestador.objects.all())
    nova_senha = forms.CharField(widget=forms.PasswordInput, required=False, help_text='Deixe em branco para não alterar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'