from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

# Create your models here.
class Autor(models.Model):
    nome = models.CharField(max_length=150)
    nacionalidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome
    

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE)
    genero = models.CharField(max_length=100, blank=True)
    ano_publicacao = models.DateTimeField(null=True, blank=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.ano_publicacao:
            data_atual = datetime.datetime.now().date()
            if self.ano_publicacao.date() > data_atual:
                raise ValidationError("A data de publicação não pode ser no futuro.")
            
class Usuario(AbstractUser):
    nacionalidade = models.CharField(max_length=30)

    def __str__(self):
        return self.username
    
    
class Perfil(models.Model):
    ROLE_CHOICES = (
        ('bibliotecario', 'Bibliotecário'),
        ('aluno', 'Aluno'),
        ('visitante', 'Visitante'),
    )
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitante')
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
class Emprestimo(models.Model):
    status_livro = (
        ('',''),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='emprestimos')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='emprestimos')
    data_emprestimo = models.DateField(default=timezone.now())
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(blank=True, null=True)
    status = models

    def __str__(self):
        return f'{self.usuario.username} - {self.livro.titulo}'
    
    @property
    def esta_atrasado(self):
        if self.data_devolucao_real:
            return self.data_devolucao_real > self.data_devolucao_prevista
        return timezone.now().date() > self.data_devolucao_prevista
    
