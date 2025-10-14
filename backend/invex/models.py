# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# ---------------------------
# MANAGER para el usuario
# ---------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# ---------------------------
# USUARIO
# ---------------------------
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# ---------------------------
# EMPRESA
# ---------------------------
class Empresa(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        Usuario,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="empresas_propietarias"
    )

    def __str__(self):
        return self.nombre

# ---------------------------
# RELACIÓN Usuario <-> Empresa con ROL
# ---------------------------
class UsuarioEmpresa(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('manager', 'Manager'),
        ('worker', 'Worker'),
        ('viewer', 'Viewer'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='relaciones')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='miembros')
    rol = models.CharField(max_length=20, choices=ROLES, default='viewer')

    class Meta:
        unique_together = ('usuario', 'empresa')
        verbose_name = "Relación Usuario-Empresa"
        verbose_name_plural = "Relaciones Usuario-Empresa"

    def __str__(self):
        return f"{self.usuario.email} en {self.empresa.nombre} como {self.get_rol_display()}"

# ---------------------------
# SUSCRIPCIÓN
# ---------------------------
class Suscripcion(models.Model):
    TIPOS = [
        ('3m', '3 Meses'),
        ('6m', '6 Meses'),
        ('1y', '1 Año'),
    ]
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, related_name='suscripcion')
    tipo = models.CharField(max_length=2, choices=TIPOS)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField()
    pago_por = models.ForeignKey(
        Usuario,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Usuario que paga la suscripción"
    )

    def __str__(self):
        return f"{self.empresa.nombre} - {self.get_tipo_display()}"

# ---------------------------
# CATEGORÍAS, PRODUCTOS Y STOCK
# ---------------------------
class Categoria(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias')
    nombre = models.CharField(max_length=255)

    class Meta:
        unique_together = ('empresa', 'nombre')
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True)
    unidad_medida = models.CharField(max_length=50, default='unidades')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    
    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='stocks')
    stock_actual = models.PositiveIntegerField(default=0)
    stock_transito = models.PositiveIntegerField(default=0)
    ventas_proyectadas = models.PositiveIntegerField(default=0)
    demanda_estacional = models.CharField(max_length=100, default="Normal")
    fecha_entrega_aprox = models.DateField(null=True, blank=True)

    # --- LÓGICA DE PROYECCIÓN AÑADIDA ---
    SEMANAS_DE_SEGURIDAD = 2
    SEMANAS_OBJETIVO = 4

    @property
    def stock_total_disponible(self):
        """Calcula el stock real más lo que viene en camino."""
        return self.stock_actual + self.stock_transito

    @property
    def semanas_de_stock(self):
        """Calcula para cuántas semanas nos alcanza el stock total disponible."""
        if self.ventas_proyectadas > 0:
            return self.stock_total_disponible / self.ventas_proyectadas
        return float('inf')  # Si no hay ventas, el stock es teóricamente infinito.

    @property
    def proyeccion_status(self):
        """Determina si es necesario comprar y devuelve un estado."""
        if self.semanas_de_stock <= self.SEMANAS_DE_SEGURIDAD:
            return "Comprar Ahora"
        elif self.semanas_de_stock <= self.SEMANAS_DE_SEGURIDAD + 1:  # Umbral de advertencia
            return "Revisar Pronto"
        else:
            return "Stock OK"

    @property
    def proyeccion_cantidad_a_comprar(self):
        """Calcula cuántas unidades se recomienda comprar."""
        if self.proyeccion_status == "Comprar Ahora":
            stock_objetivo = self.ventas_proyectadas * self.SEMANAS_OBJETIVO
            cantidad_necesaria = stock_objetivo - self.stock_total_disponible
            return max(0, round(cantidad_necesaria))
        return 0
    # --- FIN DE LA LÓGICA DE PROYECCIÓN ---

    def __str__(self):
        return f"{self.producto.nombre}: {self.stock_actual}"

# ---------------------------
# DÍAS IMPORTANTES
# ---------------------------
class DiaImportante(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='dias_importantes')
    nombre_evento = models.CharField(max_length=255)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.nombre_evento} ({self.empresa.nombre})"