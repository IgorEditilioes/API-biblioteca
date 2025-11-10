from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers, status
from .models import Usuario, Livro, Autor, Emprestimo
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
        exclude = ['id']
        read_only_fields = ['disponivel'] 
    


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['nome']

class EmprestimoSerializer(serializers.ModelSerializer):
    esta_atrasado = serializers.SerializerMethodField()
    usuario = serializers.SerializerMethodField()
    livro = serializers.SerializerMethodField()

    class Meta:
        model = Emprestimo
        exclude = []
        read_only_fields = ['data_devolucao_prevista', 'data_devolucao_real', 'usuario', 'data_emprestimo']

    def get_usuario(self, obj):
        return obj.usuario.username
    
    def get_livro(self, obj):
        return obj.livro.titulo


    def get_esta_atrasado(self, obj):
        if obj.data_devolucao_real:
            return obj.data_devolucao_real > obj.data_devolucao_prevista
        return timezone.now().date() > obj.data_devolucao_prevista

    def create(self, validated_data):
        data_emprestimo = validated_data.get('data_emprestimo', timezone.now().date())
        validated_data['data_emprestimo'] = data_emprestimo
        validated_data['data_devolucao_prevista'] = data_emprestimo + timedelta(days=7)

        livro = validated_data['livro']
        if not livro.disponivel:
            raise serializers.ValidationError('Livro indisponível para empréstimo.')

        # Atualiza o status
        livro.disponivel = False
        livro.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        data_devolucao_real = validated_data.get('data_devolucao_real')
        if data_devolucao_real:
            instance.livro.disponivel = True
            instance.livro.save()
        return super().update(instance, validated_data)
        
    
    
