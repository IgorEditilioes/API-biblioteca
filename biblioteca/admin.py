from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Livro, Autor, Emprestimo

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {'fields': ('nacionalidade',)}),
    )

class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'genero', 'ano_publicacao')
    list_display_links = ('titulo',)

admin.site.register(Livro, LivroAdmin)

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nacionalidade')
    list_display_links = ('nome',)

admin.site.register(Autor, AutorAdmin)

class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livro', 'data_emprestimo', 'data_devolucao_prevista')
    list_display_links = ('usuario',)

admin.site.register(Emprestimo, EmprestimoAdmin)