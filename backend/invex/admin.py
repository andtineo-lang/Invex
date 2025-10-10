

from django.contrib import admin
from .models import Usuario, Empresa, UsuarioEmpresa, Producto, Stock, Suscripcion, DiaImportante

# Registramos cada modelo para que aparezca en el panel de admin
admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(UsuarioEmpresa) 
admin.site.register(Producto)
admin.site.register(Stock)
admin.site.register(Suscripcion)
admin.site.register(DiaImportante)