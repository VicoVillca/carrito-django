from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'marcas', views.MarcaViewSet)
router.register(r'articulos', views.ArticuloViewSet)
router.register(r'carritos', views.CarritoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
