from rest_framework import viewsets
from .serializers import AutorSerializer, LivroSerializer, EmprestimoSerializer, UsuarioSerializer
from .models import Autor, Livro, Emprestimo, Usuario

# Create your views here.
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all().order_by('nome')
    serializer_class = AutorSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all().order_by('data_emprestimo')
    serializer_class = EmprestimoSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer