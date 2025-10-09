from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from accounts.models import UserProfile

class Command(BaseCommand):
    help = "Crea usuarios de prueba para Dulcería Lilis"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Creando usuarios de prueba para Dulcería Lilis...")
        
        usuarios_data = [
            {
                'username': 'admin_lilis',
                'email': 'admin@lilis.cl',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'password': 'admin123',
                'rol': 'Administrador',
                'rut': '11111111-1',
                'telefono': '+56912345601',
                'area': 'Administración',
                'direccion': 'Av. Amanecer 2030, Coquimbo',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'compras_lilis',
                'email': 'compras@lilis.cl',
                'first_name': 'María',
                'last_name': 'González',
                'password': 'compras123',
                'rol': 'Operador de Compras',
                'rut': '22222222-2',
                'telefono': '+56912345602',
                'area': 'Compras y Abastecimiento',
                'direccion': 'Av. Amanecer 2030, Coquimbo',
                'is_staff': True
            },
            {
                'username': 'inventario_lilis',
                'email': 'inventario@lilis.cl',
                'first_name': 'Carlos',
                'last_name': 'Rojas',
                'password': 'inventario123',
                'rol': 'Operador de Inventario',
                'rut': '33333333-3',
                'telefono': '+56912345603',
                'area': 'Bodega e Inventario',
                'direccion': 'Av. Amanecer 2030, Coquimbo',
                'is_staff': True
            },
            {
                'username': 'produccion_lilis',
                'email': 'produccion@lilis.cl',
                'first_name': 'Ana',
                'last_name': 'Muñoz',
                'password': 'produccion123',
                'rol': 'Operador de Producción',
                'rut': '44444444-4',
                'telefono': '+56912345604',
                'area': 'Planta Producción',
                'direccion': 'Av. Amanecer 2030, Coquimbo',
                'is_staff': True
            },
            {
                'username': 'ventas_lilis',
                'email': 'ventas@lilis.cl',
                'first_name': 'Luis',
                'last_name': 'Pérez',
                'password': 'ventas123',
                'rol': 'Operador de Ventas',
                'rut': '55555555-5',
                'telefono': '+56912345605',
                'area': 'Ventas y Distribución',
                'direccion': 'Av. Amanecer 2030, Coquimbo',
                'is_staff': True
            },
            {
                'username': 'finanzas_lilis',
                'email': 'finanzas@lilis.cl',
                'first_name': 'Patricia',
                'last_name': 'Silva',
                'password': 'finanzas123',
                'rol': 'Analista Financiero',
                'rut': '66666666-6',
                'telefono': '+56912345606',
                'area': 'Finanzas y Costos',
                'direccion': 'Av. Amanecer 2030, Coquimbo',
                'is_staff': True
            },
        ]
        
        for data in usuarios_data:
            # Crear o actualizar usuario
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_staff': data.get('is_staff', False),
                    'is_superuser': data.get('is_superuser', False)
                }
            )
            
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(f"✓ Usuario creado: {user.username}")
            else:
                # Actualizar password si ya existe
                user.set_password(data['password'])
                user.email = data['email']
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.is_staff = data.get('is_staff', False)
                user.is_superuser = data.get('is_superuser', False)
                user.save()
                self.stdout.write(f"- Usuario actualizado: {user.username}")
            
            # Crear o actualizar perfil
            profile, p_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'rut': data['rut'],
                    'telefono': data.get('telefono', ''),
                    'area': data['area'],
                    'direccion': data.get('direccion', '')
                }
            )
            
            if not p_created:
                # Actualizar perfil existente
                profile.rut = data['rut']
                profile.telefono = data.get('telefono', '')
                profile.area = data['area']
                profile.direccion = data.get('direccion', '')
                profile.save()
            
            # Asignar rol (group)
            try:
                group = Group.objects.get(name=data['rol'])
                user.groups.clear()
                user.groups.add(group)
                self.stdout.write(f"  → Rol asignado: {data['rol']}")
            except Group.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠ Grupo '{data['rol']}' no existe. Ejecuta setup_roles_dulceria primero.")
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Usuarios de prueba creados/actualizados exitosamente')
        )
        self.stdout.write("\nCredenciales de acceso:")
        self.stdout.write("------------------------")
        for data in usuarios_data:
            self.stdout.write(f"{data['username']} / {data['password']} → {data['rol']}")