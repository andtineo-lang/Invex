from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Producto, HistorialInventario

@receiver(post_save, sender=Producto)
def registrar_cambio_producto(sender, instance, created, **kwargs):
    # Verificamos si el producto tiene empresa asignada para evitar errores
    if not instance.empresa:
        return

    if created:
        accion = 'CREACION'
        detalle = f"Se creó el producto '{instance.nombre}' con stock inicial."
    else:
        accion = 'EDICION'
        detalle = f"Se actualizó el producto '{instance.nombre}'."

    # AQUÍ ESTABA EL ERROR: Debemos pasar 'empresa=instance.empresa'
    HistorialInventario.objects.create(
        empresa=instance.empresa,  # <--- ESTA LÍNEA ES CRUCIAL
        accion=accion,
        producto_nombre=instance.nombre,
        detalle=detalle
    )

@receiver(post_delete, sender=Producto)
def registrar_eliminacion_producto(sender, instance, **kwargs):
    if not instance.empresa:
        return

    HistorialInventario.objects.create(
        empresa=instance.empresa, # <--- AQUÍ TAMBIÉN
        accion='ELIMINACION',
        producto_nombre=instance.nombre,
        detalle="El producto fue eliminado permanentemente."
    )