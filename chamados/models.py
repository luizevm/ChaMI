from django.db import models

class Imovel(models.Model):
    endereco = models.CharField(max_length=255)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    inquilino = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.endereco
    
class Prestador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} - {self.area}'

class Chamado(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    data_abertura = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    prestador = models.ForeignKey(Prestador, on_delete=models.SET_NULL, blank=True, null=True)
    orcamento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    anexo = models.FileField(upload_to='anexos/', blank=True, null=True)

    def __str__(self):
        return f'Chamado #{self.id} - {self.imovel}'