# invex/permissions.py
from rest_framework import permissions
from .models import UsuarioEmpresa

class HasRole(permissions.BasePermission):
    def has_permission(self, request, view):
        # 1. Validar autenticación
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Buscar relación con la empresa
        # Intenta por URL (empresa_id) o toma la primera disponible
        empresa_id = view.kwargs.get('empresa_id')
        if empresa_id:
            try:
                relacion = UsuarioEmpresa.objects.get(usuario=request.user, empresa_id=empresa_id)
            except UsuarioEmpresa.DoesNotExist:
                return False
        else:
            relacion = request.user.relaciones.first()
            if not relacion:
                return False

        user_role = relacion.rol

        # 3. REGLA DE ORO: El Admin entra a TODO.
        if user_role == 'admin':
            return True

        # 4. Obtener la lista de invitados de la vista
        # Si la vista no define 'allowed_roles', nadie más entra (solo admin)
        allowed_roles = getattr(view, 'allowed_roles', [])

        # 5. Verificar si el rol del usuario está invitado
        return user_role in allowed_roles