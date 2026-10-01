from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    fecha_compra = models.DateField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    # Relación uno a muchos: un proveedor tiene varias compras,
    # y cada compra pertenece a un solo proveedor
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras')

    def __str__(self):
        return f'Compra {self.id} - {self.proveedor.nombre}'