from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import AutorSerializer, LivroSerializer, EmprestimoSerializer, UsuarioSerializer
from biblioteca.models import Autor, Livro, Emprestimo, Usuario
from .permissions import IsAdminOrReadOnly, IsAdminOrOwner
from .filters import LivroFilter, EmprestimoFilter

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser


# -----------------------------
# 🔹 Autor
# -----------------------------
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all().order_by('nome')
    serializer_class = AutorSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]


# -----------------------------
# 🔹 Livro
# -----------------------------
class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    # Filtros e busca
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = LivroFilter
    ordering_fields = ['titulo', 'autor__nome']
    search_fields = ['titulo', 'autor__nome', 'genero']


# -----------------------------
# 🔹 Empréstimo
# -----------------------------
class EmprestimoViewSet(viewsets.ModelViewSet):
    serializer_class = EmprestimoSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAdminOrOwner]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = EmprestimoFilter
    ordering_fields = ['data_emprestimo', 'data_devolucao_real']
    search_fields = ['livro__titulo', 'usuario__email']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin vê todos
            return Emprestimo.objects.all().order_by('-data_emprestimo')
        # Usuário comum só vê seus empréstimos
        return Emprestimo.objects.filter(usuario=user).order_by('-data_emprestimo')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post', 'get'])
    def devolver(self, request, pk=None):
        emprestimo = self.get_object()

        if emprestimo.data_devolucao_real:
            return Response({"detail": "Este livro já foi devolvido."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_staff and emprestimo.usuario != request.user:
            return Response({"detail": "Você não tem permissão para devolver este empréstimo."}, status=status.HTTP_403_FORBIDDEN)

        emprestimo.data_devolucao_real = timezone.now().date()
        emprestimo.livro.disponivel = True
        emprestimo.livro.save()
        emprestimo.save()

        return Response(
            {"detail": f"Livro '{emprestimo.livro.titulo}' devolvido com sucesso!"},
            status=status.HTTP_200_OK
        )


# -----------------------------
# 🔹 Usuário
# -----------------------------
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]
