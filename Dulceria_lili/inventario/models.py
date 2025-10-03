from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Bodega(models.Model):
    id_bodega = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lote {self.id_lote} - {self.id_producto.nombre}"

class Costo(models.Model):
    id_costo = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Costo - {self.id_producto.nombre}"

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventario - {self.id_producto.nombre}"

class OrdenCompra(models.Model):
    id_oc = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.RESTRICT)
    fecha = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OC {self.id_oc} - {self.id_proveedor.nombre}"

class DetalleOC(models.Model):
    id_detalle_oc = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    id_oc = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"

class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    fecha = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id_pedido}"

class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"

class OrdenProductos(models.Model):
    id_orden_producto = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    id_orden = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"
