from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Module, Role, RoleModulePermission

# Inline para UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'

# Extender UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role']
    
    def get_role(self, obj):
        groups = obj.groups.all()
        return ', '.join([g.name for g in groups]) if groups else '-'
    get_role.short_description = 'Rol'

# Re-registrar User con el nuevo admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registrar Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'icon']
    search_fields = ['name', 'code']

# Registrar Role
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['group', 'descripcion']
    search_fields = ['group__name']

# Registrar RoleModulePermission
@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'module', 'can_view', 'can_add', 'can_change', 'can_delete']
    list_filter = ['role', 'module']
    search_fields = ['role__group__name', 'module__name']
