from django.db import models
from django.contrib.auth.models import User

class Imovel(models.Model):
    TIPO_CHOICES = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
        ('rural', 'Rural'),
        ('industrial', 'Industrial'),
    ]

    endereco = models.CharField(max_length=255)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='residencial')

    def __str__(self):
        return f'{self.endereco} ({self.get_tipo_display()})'

    def esta_disponivel(self):
        return not Perfil.objects.filter(imovel=self, tipo='inquilino').exists()
    
class Prestador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} - {self.area}'

class Chamado(models.Model):
    STATUS_CHOICES = [
    ('aberto', 'Aberto'),
    ('aguardando_orcamento', 'Aguardando Orçamento'),
    ('orcamento_enviado', 'Orçamento Enviado'),
    ('orcamento_aprovado', 'Orçamento Aprovado'),
    ('orcamento_reprovado', 'Orçamento Reprovado'),
    ('em_andamento', 'Em Andamento'),
    ('resolvido_internamente', 'Resolvido Internamente'),
    ('concluido', 'Concluído'),
    ('cancelado', 'Cancelado'),
]

    CATEGORIA_CHOICES = [
        ('eletrica', 'Elétrica'),
        ('hidraulica', 'Hidráulica'),
        ('estrutural', 'Estrutural'),
        ('outro', 'Outro'),
    ]

    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='aberto')
    data_abertura = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    prestador = models.ForeignKey(Prestador, on_delete=models.SET_NULL, blank=True, null=True)
    orcamento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    anexo = models.FileField(upload_to='anexos/', blank=True, null=True)

    def __str__(self):
        return f'Chamado #{self.id} - {self.imovel}'

class Perfil(models.Model):
    TIPO_CHOICES = [
        ('admin', 'Administrador'),
        ('inquilino', 'Inquilino'),
        ('prestador', 'Prestador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    imovel = models.ForeignKey(Imovel, on_delete=models.SET_NULL, blank=True, null=True)
    prestador = models.ForeignKey(Prestador, on_delete=models.SET_NULL, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} — {self.get_tipo_display()}'