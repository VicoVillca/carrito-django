from rest_framework import serializers
from .models import Marca, Articulo, Carrito, ItemCarrito

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ArticuloSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')

    class Meta:
        model = Articulo
        fields = '__all__'

class ItemCarritoSerializer(serializers.ModelSerializer):
    articulo_nombre = serializers.ReadOnlyField(source='articulo.nombre')
    precio = serializers.ReadOnlyField(source='articulo.precio')
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrito
        fields = ['id', 'carrito', 'articulo', 'articulo_nombre', 'cantidad', 'precio', 'subtotal']
        read_only_fields = ['carrito']

    def get_subtotal(self, obj):
        return obj.cantidad * obj.articulo.precio

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'estado', 'fecha_creacion', 'fecha_actualizacion', 'items', 'total']

    def get_total(self, obj):
        return sum(item.cantidad * item.articulo.precio for item in obj.items.all())
