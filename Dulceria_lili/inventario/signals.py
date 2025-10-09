from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleOC, Inventario

@receiver(post_save, sender=DetalleOC)
def actualizar_inventario(sender, instance, created, **kwargs):
    if created:
        producto = instance.id_producto
        cantidad = instance.cantidad

        inventario, creado = Inventario.objects.get_or_create(
            id_producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not creado:
            inventario.cantidad += cantidad
            inventario.save()