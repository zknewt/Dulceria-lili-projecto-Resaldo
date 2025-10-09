from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Roles del sistema
class Roles(models.Model):
    Tipo_Rol = models.SlugField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

# Usuario del sistema
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Proveedor
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="proveedor"
    )
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.usuario:
            return f"{self.nombre} (Usuario: {self.usuario.username})"
        return self.nombre

# Orden de Compra
class OrdenCompra(models.Model):
    id_oc = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.RESTRICT)
    fecha = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OC {self.id_oc} - {self.id_proveedor.nombre}"

# Producto
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_oc = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Bodega
class Bodega(models.Model):
    id_bodega = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Lote
class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lote {self.id_lote} - {self.id_producto.nombre}"

# Costo
class Costo(models.Model):
    id_costo = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Costo - {self.id_producto.nombre}"

# Inventario
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventario - {self.id_producto.nombre}"

# Detalle de Orden de Compra
class DetalleOC(models.Model):
    id_detalle_oc = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    id_oc = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"

# Pedido
class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    fecha = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id_pedido}"

# Detalle de Pedido
class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"

# Orden de Productos
class OrdenProductos(models.Model):
    id_orden_producto = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    id_orden = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"