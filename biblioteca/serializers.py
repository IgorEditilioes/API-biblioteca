from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import Usuario, Livro, Autor, Emprestimo


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'
        read_only_fields = ['disponivel'] 

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class EmprestimoSerializer(serializers.ModelSerializer):
    esta_atrasado = serializers.SerializerMethodField()

    class Meta:
        model = Emprestimo
        fields = '__all__'
        read_only_fields = ['data_devolucao_prevista', 'data_devolucao_real']


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
        
    
     # Valida a data de devolução real
    def validate_data_devolucao_real(self, value):
        if value:
            data_emprestimo = self.instance.data_emprestimo if self.instance else None
            if data_emprestimo and value < data_emprestimo:
                raise serializers.ValidationError("Data de devolução não pode ser anterior ao empréstimo.")

            # Se quiser apenas avisar (não impedir), pode logar ou retornar normalmente
            data_prevista = self.instance.data_devolucao_prevista if self.instance else None
            if data_prevista and value > data_prevista:
                # Não levanta erro — apenas sinaliza atraso
                pass
        return value
    
