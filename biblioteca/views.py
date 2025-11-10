from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .serializers import AutorSerializer, LivroSerializer, EmprestimoSerializer, UsuarioSerializer
from .models import Autor, Livro, Emprestimo, Usuario
from .permissions import IsAdminOrReadOnly, IsAdminOrAuthenticatedReadOnly, IsAdminOrOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

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

       # 🔍 Filtros — permitem filtrar por campos específicos, inclusive FK
    filterset_fields = {
        'titulo': ['exact', 'icontains'],
        'autor__nome': ['exact', 'icontains'],  # FK -> busca por nome do autor
        'disponivel': ['exact'],
        'genero': ['exact', 'icontains'],
    }

    # 🔠 Ordenação — pode ordenar pelo título ou nome do autor
    ordering_fields = ['titulo', 'autor__nome']

    # 🔎 Busca textual — procura por texto parcial no título, nome do autor ou gênero
    search_fields = ['titulo', 'autor__nome', 'genero']


# -----------------------------
# 🔹 Empréstimo
# -----------------------------
class EmprestimoViewSet(viewsets.ModelViewSet):
    serializer_class = EmprestimoSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAdminOrOwner]

    # ✅ Adiciona filtros e ordenação
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['livro__titulo', 'usuario__email', 'usuario__username', 'data_devolucao_real', 'data_devolucao_prevista']
    ordering_fields = ['data_emprestimo', 'data_devolucao_real']
    search_fields = ['livro__titulo', 'usuario__email']

    # 🔍 Filtra os empréstimos conforme o tipo de usuário
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Emprestimo.objects.all().order_by('data_emprestimo')

        # Usuário comum vê apenas os próprios empréstimos
        return Emprestimo.objects.filter(usuario=user).order_by('data_emprestimo')

    # 🪶 Ao criar, vincula automaticamente ao usuário logado
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    # 📦 Endpoint para devolução do livro
    @action(detail=True, methods=['post', 'get'])
    def devolver(self, request, pk=None):
        emprestimo = self.get_object()

        # Bloqueia devolução duplicada
        if emprestimo.data_devolucao_real:
            return Response(
                {"detail": "Este livro já foi devolvido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Bloqueia se o usuário não for dono (a menos que seja admin)
        if not request.user.is_staff and emprestimo.usuario != request.user:
            return Response(
                {"detail": "Você não tem permissão para devolver este empréstimo."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Processa a devolução
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
