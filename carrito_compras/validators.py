from django.core.exceptions import ValidationError

def validar_precio_positivo(value):
    if value < 0:
        raise ValidationError("El precio no puede ser negativo.")

def validar_cantidad_positiva(value):
    if value <= 0:
        raise ValidationError("La cantidad debe ser mayor a cero.")
