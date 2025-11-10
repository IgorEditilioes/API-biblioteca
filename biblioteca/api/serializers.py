from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers, status
from biblioteca.models import Usuario, Livro, Autor, Emprestimo
from rest_framework.response import Response

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    autor = serializers.SlugRelatedField(
        queryset=Autor.objects.all(),   # permite enviar o ID ou nome existente
        slug_field='nome'               # mostra o nome em vez do ID
    )
    class Meta:
        model = Livro
        exclude = []
        read_only_fields = ['disponivel'] 
    


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['nome']

class EmprestimoSerializer(serializers.ModelSerializer):
    # Campos só para exibição
    livro_titulo = serializers.StringRelatedField(source='livro', read_only=True)
    usuario_nome = serializers.StringRelatedField(source='usuario', read_only=True)
    esta_atrasado = serializers.SerializerMethodField(read_only=True)

    # Campo para criação de empréstimo (escrita) — só livros disponíveis
    livro = serializers.PrimaryKeyRelatedField(
        queryset=Livro.objects.filter(disponivel=True),
        write_only=True
    )

    class Meta:
        model = Emprestimo
        fields = '__all__'
        read_only_fields = [
            'usuario',
            'data_emprestimo',
            'data_devolucao_prevista',
            'data_devolucao_real',
            'esta_atrasado',
            'usuario_nome',
            'livro_titulo'
        ]

    def get_usuario_nome(self, obj):
        return obj.usuario.username if obj.usuario else None

    def get_esta_atrasado(self, obj):
        if obj.data_devolucao_real:
            return obj.data_devolucao_real > obj.data_devolucao_prevista
        return timezone.now().date() > obj.data_devolucao_prevista

    def create(self, validated_data):
        # Define datas automáticas
        data_emprestimo = timezone.now().date()
        validated_data['data_emprestimo'] = data_emprestimo
        validated_data['data_devolucao_prevista'] = data_emprestimo + timedelta(days=7)

        livro = validated_data['livro']
        if not livro.disponivel:
            raise serializers.ValidationError('Livro indisponível para empréstimo.')

        # Atualiza disponibilidade do livro
        livro.disponivel = False
        livro.save()

        return super().create(validated_data)