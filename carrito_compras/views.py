from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Marca, Articulo, Carrito, ItemCarrito
from .serializers import MarcaSerializer, ArticuloSerializer, CarritoSerializer, ItemCarritoSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class ArticuloViewSet(viewsets.ModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        carrito = self.get_object()
        if carrito.estado != 'abierto':
            return Response({'error': 'El carrito ya está pagado o cancelado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not carrito.items.exists():
            return Response({'error': 'No se puede procesar un carrito vacío.'}, status=status.HTTP_400_BAD_REQUEST)

        carrito.estado = 'pagado'
        carrito.save()

        for item in carrito.items.all():
            if item.articulo.stock >= item.cantidad:
                item.articulo.stock -= item.cantidad
                item.articulo.save()
            else:
                continue

        serializer = self.get_serializer(carrito)
        return Response({
            'message': 'Pago procesado y carrito cerrado exitosamente.',
            'carrito': serializer.data
        })

    @action(detail=True, methods=['post'])
    def agregar_item(self, request, pk=None):
        carrito = self.get_object()
        if carrito.estado != 'abierto':
            return Response({'error': 'No se pueden agregar items a un carrito cerrado.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ItemCarritoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(carrito=carrito)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
