from django.contrib import admin
from .models import Marca, Articulo, Carrito, ItemCarrito

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'precio', 'stock')
    list_filter = ('marca',)
    search_fields = ('nombre',)

class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 1

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('estado',)
    inlines = [ItemCarritoInline]

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrito', 'articulo', 'cantidad')
