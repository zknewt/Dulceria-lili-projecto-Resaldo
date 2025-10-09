from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Module, Role, RoleModulePermission

class Command(BaseCommand):
    help = "Configura roles y permisos para Dulcería Lilis"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando configuración de roles y permisos...")
        
        # 1. Crear Módulos
        self.stdout.write("\n1. Creando Módulos del Sistema...")
        modulos_data = [
            ('inventario', 'Inventario', 'fa-box', 'Gestión de productos, lotes y bodegas'),
            ('compras', 'Compras y Proveedores', 'fa-shopping-cart', 'OC, proveedores y recepciones'),
            ('produccion', 'Producción', 'fa-industry', 'Órdenes producción, BOM, mermas'),
            ('ventas', 'Ventas y Clientes', 'fa-cash-register', 'Pedidos, cotizaciones, facturación'),
            ('costos', 'Costos y Finanzas', 'fa-chart-line', 'Costos, precios y análisis financiero'),
        ]
        
        for code, name, icon, desc in modulos_data:
            module, created = Module.objects.get_or_create(
                code=code,
                defaults={'name': name, 'icon': icon, 'descripcion': desc}
            )
            if created:
                self.stdout.write(f"   ✓ Módulo creado: {name}")
            else:
                self.stdout.write(f"   - Módulo ya existe: {name}")
        
        # 2. Crear Roles (Groups)
        self.stdout.write("\n2. Creando Roles del Sistema...")
        roles_data = [
            ('Administrador', 'Control total del sistema ERP'),
            ('Operador de Compras', 'Gestión de compras y proveedores'),
            ('Operador de Inventario', 'Control de stock y trazabilidad'),
            ('Operador de Producción', 'Órdenes de producción y mermas'),
            ('Operador de Ventas', 'Gestión de ventas y clientes'),
            ('Analista Financiero', 'Costos, precios y reportes financieros'),
        ]
        
        for nombre, descripcion in roles_data:
            group, g_created = Group.objects.get_or_create(name=nombre)
            role, r_created = Role.objects.get_or_create(
                group=group,
                defaults={'descripcion': descripcion}
            )
            if r_created:
                self.stdout.write(f"   ✓ Rol creado: {nombre}")
            else:
                self.stdout.write(f"   - Rol ya existe: {nombre}")
        
        # 3. Asignar Permisos por Rol
        self.stdout.write("\n3. Configurando Permisos por Rol...")
        self.setup_permisos()
        self.asignar_permisos_django()
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Roles y permisos configurados exitosamente')
        )
    
    def setup_permisos(self):
        """Configurar matriz de permisos según roles"""
        
        # Obtener todos los módulos
        inventario = Module.objects.get(code='inventario')
        compras = Module.objects.get(code='compras')
        produccion = Module.objects.get(code='produccion')
        ventas = Module.objects.get(code='ventas')
        costos = Module.objects.get(code='costos')
        
        # Obtener todos los roles
        admin_role = Role.objects.get(group__name='Administrador')
        compras_role = Role.objects.get(group__name='Operador de Compras')
        inventario_role = Role.objects.get(group__name='Operador de Inventario')
        produccion_role = Role.objects.get(group__name='Operador de Producción')
        ventas_role = Role.objects.get(group__name='Operador de Ventas')
        financiero_role = Role.objects.get(group__name='Analista Financiero')
        
        # ADMINISTRADOR: CRUD completo en TODO
        self.stdout.write("   Configurando: Administrador")
        for module in [inventario, compras, produccion, ventas, costos]:
            RoleModulePermission.objects.update_or_create(
                role=admin_role,
                module=module,
                defaults={
                    'can_view': True,
                    'can_add': True,
                    'can_change': True,
                    'can_delete': True
                }
            )
        
        # OPERADOR DE COMPRAS: CRUD Compras, Ver Inventario
        self.stdout.write("   Configurando: Operador de Compras")
        RoleModulePermission.objects.update_or_create(
            role=compras_role, module=compras,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': True}
        )
        RoleModulePermission.objects.update_or_create(
            role=compras_role, module=inventario,
            defaults={'can_view': True, 'can_add': False, 'can_change': False, 'can_delete': False}
        )
        
        # OPERADOR DE INVENTARIO: CRUD Inventario, Ver Compras
        self.stdout.write("   Configurando: Operador de Inventario")
        RoleModulePermission.objects.update_or_create(
            role=inventario_role, module=inventario,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': True}
        )
        RoleModulePermission.objects.update_or_create(
            role=inventario_role, module=compras,
            defaults={'can_view': True, 'can_add': False, 'can_change': False, 'can_delete': False}
        )
        
        # OPERADOR DE PRODUCCIÓN: CRUD Producción (sin Delete), Ver/Editar Inventario
        self.stdout.write("   Configurando: Operador de Producción")
        RoleModulePermission.objects.update_or_create(
            role=produccion_role, module=produccion,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': False}
        )
        RoleModulePermission.objects.update_or_create(
            role=produccion_role, module=inventario,
            defaults={'can_view': True, 'can_add': False, 'can_change': True, 'can_delete': False}
        )
        
        # OPERADOR DE VENTAS: CRUD Ventas, Ver Inventario
        self.stdout.write("   Configurando: Operador de Ventas")
        RoleModulePermission.objects.update_or_create(
            role=ventas_role, module=ventas,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': True}
        )
        RoleModulePermission.objects.update_or_create(
            role=ventas_role, module=inventario,
            defaults={'can_view': True, 'can_add': False, 'can_change': False, 'can_delete': False}
        )
        
        # ANALISTA FINANCIERO: CRUD Costos, Ver todos los demás
        self.stdout.write("   Configurando: Analista Financiero")
        RoleModulePermission.objects.update_or_create(
            role=financiero_role, module=costos,
            defaults={'can_view': True, 'can_add': True, 'can_change': True, 'can_delete': True}
        )
        for module in [inventario, compras, produccion, ventas]:
            RoleModulePermission.objects.update_or_create(
                role=financiero_role, module=module,
                defaults={'can_view': True, 'can_add': False, 'can_change': False, 'can_delete': False}
            )
        
        self.stdout.write("   ✓ Permisos asignados según matriz de roles")

    def asignar_permisos_django(self):
        
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Permission, Group

        def get_ct_or_raise(app_label, model_name):
            try:
                return ContentType.objects.get(app_label=app_label, model=model_name)
            except ContentType.DoesNotExist:
                raise RuntimeError(
                    f"ContentType no encontrado: app_label='{app_label}', model='{model_name}'. "
                    "Verifica que el modelo exista y las migraciones estén aplicadas."
                )

    
        ct_producto = get_ct_or_raise('inventario', 'producto')
        ct_proveedor = get_ct_or_raise('inventario', 'proveedor')
        ct_bodega = get_ct_or_raise('inventario', 'bodega')
        ct_ordencompra = get_ct_or_raise('inventario', 'ordencompra')
        ct_detalleoc = get_ct_or_raise('inventario', 'detalleoc')
        ct_pedido = get_ct_or_raise('inventario', 'pedidos')            
        ct_detallepedido = get_ct_or_raise('inventario', 'detallepedido')
        ct_ordenproduccion = get_ct_or_raise('inventario', 'ordenproductos') 
        ct_lote = get_ct_or_raise('inventario', 'lote')
        ct_inventario = get_ct_or_raise('inventario', 'inventario')
        ct_costo = get_ct_or_raise('inventario', 'costo')

        # OPERADOR DE COMPRAS: Proveedores, OrdenCompra, DetalleOC
        compras_group = Group.objects.get(name='Operador de Compras')
        compras_perms = Permission.objects.filter(
            content_type__in=[ct_proveedor, ct_ordencompra, ct_detalleoc]
        )
        compras_group.permissions.set(compras_perms)
        # Solo VIEW en productos
        compras_group.permissions.add(
            Permission.objects.get(codename='view_producto', content_type=ct_producto)
        )

        # OPERADOR DE INVENTARIO: Productos, Bodega, Lote, Inventario
        inventario_group = Group.objects.get(name='Operador de Inventario')
        inventario_perms = Permission.objects.filter(
            content_type__in=[ct_producto, ct_bodega, ct_lote, ct_inventario]
        )
        inventario_group.permissions.set(inventario_perms)

        # OPERADOR DE PRODUCCIÓN: OrdenProductos
        produccion_group = Group.objects.get(name='Operador de Producción')
        produccion_perms = Permission.objects.filter(
            content_type=ct_ordenproduccion
        ).exclude(codename='delete_ordenproductos') 
        produccion_group.permissions.set(produccion_perms)
        # Editar inventario 
        produccion_group.permissions.add(
            Permission.objects.get(codename='view_inventario', content_type=ct_inventario),
            Permission.objects.get(codename='change_inventario', content_type=ct_inventario)
        )

        # OPERADOR DE VENTAS: Pedidos, DetallePedido
        ventas_group = Group.objects.get(name='Operador de Ventas')
        ventas_perms = Permission.objects.filter(
            content_type__in=[ct_pedido, ct_detallepedido]
        )
        ventas_group.permissions.set(ventas_perms)
        # Ver productos
        ventas_group.permissions.add(
            Permission.objects.get(codename='view_producto', content_type=ct_producto)
        )

        # ANALISTA FINANCIERO: Costo + Ver todo
        financiero_group = Group.objects.get(name='Analista Financiero')
        costo_perms = Permission.objects.filter(content_type=ct_costo)
        financiero_group.permissions.set(costo_perms)
        # Ver todos los demás 
        for ct in [ct_producto, ct_proveedor, ct_ordencompra, ct_pedido, ct_ordenproduccion]:
            financiero_group.permissions.add(
                Permission.objects.get(codename=f'view_{ct.model}', content_type=ct)
            )

        self.stdout.write("   ✓ Permisos de Django asignados a los grupos")

