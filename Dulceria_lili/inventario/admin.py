from django.contrib import admin
from .models import (
    Proveedor, Producto, Bodega, Usuario, Lote, Inventario,
    Costo, OrdenCompra, DetalleOC, Pedidos, DetallePedido, OrdenProductos
)

# Inlines
class DetalleOCInline(admin.TabularInline):
    model = DetalleOC
    extra = 1
    fields = ("id_producto", "cantidad")
    show_change_link = True

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1
    fields = ("id_producto", "cantidad")
    show_change_link = True

class OrdenProductosInline(admin.TabularInline):
    model = OrdenProductos
    extra = 1
    fields = ("id_producto", "cantidad")
    show_change_link = True

# Registro de modelos
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'nombre', 'apellido', 'correo', 'create_at']
    list_filter = ['create_at']
    search_fields = ['nombre', 'apellido', 'correo']
    ordering = ['-create_at']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['id_proveedor', 'nombre', 'direccion', 'telefono', 'create_at']
    list_filter = ['create_at']
    search_fields = ['nombre', 'telefono']
    ordering = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'nombre', 'descripcion', 'create_at']
    list_filter = ['create_at']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    inlines = [DetalleOCInline]

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['id_bodega', 'nombre', 'create_at']
    search_fields = ['nombre']
    ordering = ['nombre']

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['id_lote', 'id_producto', 'fecha_vencimiento', 'cantidad', 'create_at']
    list_filter = ['fecha_vencimiento', 'create_at']
    search_fields = ['id_producto__nombre']
    ordering = ['-fecha_vencimiento']

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['id_inventario', 'id_producto', 'cantidad', 'create_at']
    list_filter = ['create_at']
    search_fields = ['id_producto__nombre']
    ordering = ['-create_at']


@admin.register(Costo)
class CostoAdmin(admin.ModelAdmin):
    list_display = ['id_costo', 'id_producto', 'costo_unitario', 'create_at']
    list_filter = ['create_at']
    search_fields = ['id_producto__nombre']
    ordering = ['-create_at']

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id_oc', 'id_usuario', 'id_proveedor', 'fecha', 'create_at']
    list_filter = ['fecha', 'create_at']
    search_fields = ['id_proveedor__nombre']
    ordering = ['-fecha']
    inlines = [DetalleOCInline]

@admin.register(DetalleOC)
class DetalleOCAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_oc', 'id_oc', 'id_producto', 'cantidad', 'create_at']
    list_filter = ['create_at']
    search_fields = ['id_oc__id_oc', 'id_producto__nombre']
    ordering = ['-create_at']

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'id_usuario', 'fecha', 'create_at']
    list_filter = ['fecha', 'create_at']
    search_fields = ['id_usuario__nombre']
    ordering = ['-fecha']
    inlines = [DetallePedidoInline, OrdenProductosInline]

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_pedido', 'id_pedido', 'id_producto', 'cantidad', 'create_at']
    list_filter = ['create_at']
    search_fields = ['id_pedido__id_pedido', 'id_producto__nombre']
    ordering = ['-create_at']

@admin.register(OrdenProductos)
class OrdenProductosAdmin(admin.ModelAdmin):
    list_display = ['id_orden_producto', 'id_orden', 'id_producto', 'cantidad', 'create_at']
    list_filter = ['create_at']
    search_fields = ['id_producto__nombre']
    ordering = ['-create_at']
