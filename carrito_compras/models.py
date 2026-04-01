from django.db import models
from .validators import validar_precio_positivo, validar_cantidad_positiva

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Articulo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='articulos')
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_precio_positivo])
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.marca.nombre})"

class Carrito(models.Model):
    ESTADOS = [
        ('abierto', 'Abierto'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='abierto')

    def __str__(self):
        return f"Carrito #{self.id} - {self.get_estado_display()}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, validators=[validar_cantidad_positiva])

    def __str__(self):
        return f"{self.cantidad} x {self.articulo.nombre} en Carrito #{self.carrito.id}"
