from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey('inventario.Usuario', on_delete=models.PROTECT, null=True, blank=True)
    id_proveedor = models.ForeignKey('inventario.Proveedor', on_delete=models.PROTECT, null=True, blank=True)
    rol = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"