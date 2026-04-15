from django.db import models

class Imovel(models.Model):
    endereco = models.CharField(max_length=255)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    inquilino = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.endereco

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

    def __str__(self):
        return f'Chamado #{self.id} - {self.imovel}'