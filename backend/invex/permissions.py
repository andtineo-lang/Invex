# invex/permissions.py

from rest_framework import permissions
from .models import UsuarioEmpresa

class HasRole(permissions.BasePermission):
    """
    Permiso personalizado para verificar si un usuario tiene un rol específico
    o roles superiores dentro de la empresa actual.
    """
    
    # Definimos la jerarquía de roles
    ROLE_HIERARCHY = {
        'viewer': 1,
        'worker': 2,
        'manager': 3,
        'admin': 4,
    }

    def has_permission(self, request, view):
        # Primero, verificamos que el usuario esté autenticado
        if not request.user or not request.user.is_authenticated:
            return False

        # Extraemos el rol mínimo requerido desde la vista
        required_roles = getattr(view, 'required_roles', None)
        if not required_roles:
            return True # Si la vista no especifica roles, se permite el acceso

        # Obtenemos el rol del usuario en la empresa actual
        # Asumimos que la empresa se pasa en la URL (ej: /api/empresas/<empresa_id>/...)
        # Si no, necesitaremos una lógica para encontrar la empresa activa
        empresa_id = view.kwargs.get('empresa_id')
        if not empresa_id:
            # Fallback si no hay empresa_id en la URL
            relacion = UsuarioEmpresa.objects.filter(usuario=request.user).first()
            if not relacion:
                return False
            user_role = relacion.rol
        else:
            try:
                relacion = UsuarioEmpresa.objects.get(usuario=request.user, empresa_id=empresa_id)
                user_role = relacion.rol
            except UsuarioEmpresa.DoesNotExist:
                return False # El usuario no pertenece a esta empresa
        
        # Comparamos el nivel jerárquico del usuario con el mínimo requerido
        user_level = self.ROLE_HIERARCHY.get(user_role, 0)
        
        # Buscamos el nivel más bajo permitido por la vista
        required_level = min([self.ROLE_HIERARCHY.get(role, 5) for role in required_roles])

        return user_level >= required_level