from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

class UserProfile(models.Model):
    """
    Perfil extendido de usuario con datos específicos de Dulcería Lilis
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    area = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Área de trabajo: Producción, Ventas, Finanzas, etc."
    )
    
    def __str__(self):
        if self.user.get_full_name():
            return f"{self.user.get_full_name()} - {self.user.username}"
        return self.user.username
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"


class Module(models.Model):
    """
    Módulos del sistema ERP Dulcería Lilis
    """
    MODULES_CHOICES = [
        ('inventario', 'Inventario'),
        ('compras', 'Compras y Proveedores'),
        ('produccion', 'Producción'),
        ('ventas', 'Ventas y Clientes'),
        ('costos', 'Costos y Finanzas'),
    ]
    
    code = models.SlugField(
        max_length=50, 
        unique=True,
        choices=MODULES_CHOICES
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Clase CSS para icono"
    )
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos del Sistema"


class Role(models.Model):
    """
    Rol del sistema vinculado a Group de Django
    """
    group = models.OneToOneField(
        Group, 
        on_delete=models.CASCADE,
        related_name="role"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción detallada del rol"
    )
    
    def __str__(self):
        return self.group.name
    
    class Meta:
        verbose_name = "Rol del Sistema"
        verbose_name_plural = "Roles del Sistema"


class RoleModulePermission(models.Model):
    """
    Permisos específicos de cada Rol para cada Módulo
    """
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE,
        related_name="module_perms"
    )
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE,
        related_name="role_perms"
    )
    
    # Permisos CRUD
    can_view = models.BooleanField(default=False, verbose_name="Ver")
    can_add = models.BooleanField(default=False, verbose_name="Crear")
    can_change = models.BooleanField(default=False, verbose_name="Editar")
    can_delete = models.BooleanField(default=False, verbose_name="Eliminar")
    
    class Meta:
        unique_together = ("role", "module")
        verbose_name = "Permiso Rol-Módulo"
        verbose_name_plural = "Permisos Rol-Módulo"
    
    def __str__(self):
        perms = []
        if self.can_view: perms.append("Ver")
        if self.can_add: perms.append("Crear")
        if self.can_change: perms.append("Editar")
        if self.can_delete: perms.append("Eliminar")
        perms_str = ', '.join(perms) if perms else 'Sin permisos'
        return f"{self.role} → {self.module} ({perms_str})"