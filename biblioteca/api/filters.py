import django_filters
from biblioteca.models import Livro, Emprestimo


# -----------------------------
# 🔹 Filtro para Livro
# -----------------------------
class LivroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    autor__nome = django_filters.CharFilter(lookup_expr='icontains')
    genero = django_filters.CharFilter(lookup_expr='icontains')
    disponivel = django_filters.BooleanFilter()

    class Meta:
        model = Livro
        fields = ['titulo', 'autor__nome', 'genero', 'disponivel']


# -----------------------------
# 🔹 Filtro para Empréstimo
# -----------------------------
class EmprestimoFilter(django_filters.FilterSet):
    livro__titulo = django_filters.CharFilter(lookup_expr='icontains')
    usuario__email = django_filters.CharFilter(lookup_expr='icontains')
    usuario__username = django_filters.CharFilter(lookup_expr='icontains')
    data_devolucao_prevista = django_filters.DateFilter()
    data_devolucao_real = django_filters.DateFilter()

    class Meta:
        model = Emprestimo
        fields = [
            'livro__titulo',
            'usuario__email',
            'usuario__username',
            'data_devolucao_prevista',
            'data_devolucao_real',
        ]
