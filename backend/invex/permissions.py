# invex/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import UsuarioEmpresa


class RolePermission(BasePermission):
    """
    Permiso genérico basado en el rol del usuario dentro de la empresa.
    La vista debe definir un dict `role_perms` con llaves:
      - 'read'   -> métodos seguros (GET, HEAD, OPTIONS)
      - 'write'  -> POST, PUT, PATCH
      - 'delete' -> DELETE

    Ejemplo en la vista:
    role_perms = {
        'read':   ['admin', 'manager', 'worker', 'viewer'],
        'write':  ['admin', 'manager'],
        'delete': ['admin'],
    }
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Debe estar vinculado al menos a una empresa
        relacion = user.relaciones.first()
        if not relacion:
            return False

        rol = relacion.rol  # 'admin', 'manager', 'worker', 'viewer'

        # Si la vista no define reglas, dejamos pasar (solo IsAuthenticated se encarga)
        role_perms = getattr(view, 'role_perms', None)
        if role_perms is None:
            return True

        # Determinar el tipo de operación
        if request.method in SAFE_METHODS:
            allowed_roles = role_perms.get('read', [])
        elif request.method == 'DELETE':
            allowed_roles = role_perms.get('delete', [])
        else:
            allowed_roles = role_perms.get('write', [])

        # Permitir si la vista usa 'any'
        if allowed_roles == 'any':
            return True

        return rol in allowed_roles
