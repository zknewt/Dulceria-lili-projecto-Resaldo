from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Producto, Proveedor, OrdenCompra, DetalleOC, Inventario

# Productos
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'unidad', 'precio_base', 'cantidad_producto']
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'unidad', 'precio_base', 'cantidad_producto']
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

# Proveedores
class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'inventario/proveedor_list.html'

class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    fields = ['nombre', 'rut', 'direccion', 'contacto', 'condiciones_comerciales']
    template_name = 'inventario/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    fields = ['nombre', 'rut', 'direccion', 'contacto', 'condiciones_comerciales']
    template_name = 'inventario/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')

class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'inventario/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')

# Órdenes de compra
class OrdenCompraListView(LoginRequiredMixin, ListView):
    model = OrdenCompra
    template_name = 'inventario/ordencompra_list.html'

class OrdenCompraCreateView(LoginRequiredMixin, CreateView):
    model = OrdenCompra
    fields = ['proveedor', 'fecha', 'estado', 'total']
    template_name = 'inventario/ordencompra_form.html'
    success_url = reverse_lazy('orden_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class OrdenCompraDetailView(LoginRequiredMixin, DetailView):
    model = OrdenCompra
    template_name = 'inventario/ordencompra_detail.html'


class DetalleOCCreateView(CreateView):
    model = DetalleOC
    fields = ['id_producto', 'id_oc', 'cantidad']
    template_name = 'inventario/detalleoc_form.html'
    success_url = reverse_lazy('orden_list')  # o la vista que tú uses

    def form_valid(self, form):
        response = super().form_valid(form)

        producto = form.instance.id_producto
        cantidad = form.instance.cantidad

        inventario, creado = Inventario.objects.get_or_create(
            id_producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not creado:
            inventario.cantidad += cantidad
            inventario.save()

        return response