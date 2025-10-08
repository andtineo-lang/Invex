# invex/api.py
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UsuarioSerializer

class CustomAuthToken(ObtainAuthToken):
    """ 
    Personaliza la respuesta del login para incluir el token y los datos del usuario. 
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Obtener la relación más reciente del usuario con una empresa (para el rol)
        try:
            relacion_empresa = user.relaciones.latest('id')
            rol = relacion_empresa.rol
        except Exception:
            # En caso de que el usuario aún no tenga una relación (ej: recién creado y no ha completado el flujo)
            rol = 'n/a' 

        return Response({
            'token': token.key,
            'user': UsuarioSerializer(user).data,
            'rol': rol,
        })