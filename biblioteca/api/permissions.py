from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff
    
class IsAdminOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    - Qualquer usuário autenticado pode visualizar e criar empréstimos
    - Somente o admin pode alterar ou excluir
    """

    def has_permission(self, request, view):
        # Todos precisam estar autenticados
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Todos autenticados podem ler ou criar
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        # Somente admin pode editar ou deletar
        return request.user.is_staff
    

class IsAdminOrOwner(permissions.BasePermission):
    """
    Permite acesso total ao admin.
    Usuários comuns só podem acessar seus próprios empréstimos.
    """

    def has_permission(self, request, view):
        # Ninguém acessa nada sem estar autenticado
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin pode tudo
        if request.user.is_staff:
            return True

        # Usuário comum só pode ver/devolver seus próprios empréstimos
        return obj.usuario == request.user