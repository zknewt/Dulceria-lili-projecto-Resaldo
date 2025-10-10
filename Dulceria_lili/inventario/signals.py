from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import date

from accounts.models import UserProfile
from inventario.models import (
    Producto, Costo, Inventario, Lote,
    Pedidos, DetallePedido,
    OrdenCompra, DetalleOC
)

# 1. Crear perfil de usuario al crear User
@receiver(post_save, sender=User)
def crear_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

# 2. Crear registros relacionados al crear Producto
@receiver(post_save, sender=Producto)
def crear_registros_producto(sender, instance, created, **kwargs):
    if created:
        Costo.objects.get_or_create(
            id_producto=instance,
            defaults={'costo_unitario': 0.00}
        )
        Inventario.objects.get_or_create(
            id_producto=instance,
            defaults={'cantidad': 0.00}
        )
        Lote.objects.get_or_create(
            id_producto=instance,
            defaults={
                'cantidad': 0.00,
                'fecha_vencimiento': date(2099, 12, 31)
            }
        )

# 3. Crear detalle de pedido al crear Pedidos
@receiver(post_save, sender=Pedidos)
def crear_detalle_pedido(sender, instance, created, **kwargs):
    if created:
        producto = Producto.objects.first()
        if producto:
            DetallePedido.objects.get_or_create(
                id_pedido=instance,
                id_producto=producto,
                defaults={'cantidad': 1.00}
            )

# 4. Crear detalle de orden de compra al crear OrdenCompra
@receiver(post_save, sender=OrdenCompra)
def crear_detalle_oc(sender, instance, created, **kwargs):
    if created:
        producto = Producto.objects.first()
        if producto:
            DetalleOC.objects.get_or_create(
                id_oc=instance,
                id_producto=producto,
                defaults={'cantidad': 1.00}
            )