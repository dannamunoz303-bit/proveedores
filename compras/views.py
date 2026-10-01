from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Proveedor, Compra
from .serializers import ProveedorSerializer, CompraSerializer


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter('nombre', str, description='Buscar proveedores por nombre'),
    ])
)
class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer

    def get_queryset(self):
        queryset = Proveedor.objects.all()
        nombre = self.request.query_params.get('nombre')
        if self.action == 'list' and nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        return queryset


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter('fecha', str, description='Fecha exacta (AAAA-MM-DD)'),
        OpenApiParameter('proveedor', int, description='Id del proveedor'),
        OpenApiParameter('valor_min', float, description='Valor mínimo'),
        OpenApiParameter('valor_max', float, description='Valor máximo'),
    ])
)
class CompraViewSet(viewsets.ModelViewSet):
    serializer_class = CompraSerializer

    def get_queryset(self):
        # select_related trae el proveedor en la misma consulta (más eficiente)
        queryset = Compra.objects.select_related('proveedor')
        if self.action == 'list':
            p = self.request.query_params
            if p.get('fecha'):
                queryset = queryset.filter(fecha_compra=p['fecha'])
            if p.get('proveedor'):
                queryset = queryset.filter(proveedor_id=p['proveedor'])
            if p.get('valor_min'):
                queryset = queryset.filter(valor_total__gte=p['valor_min'])
            if p.get('valor_max'):
                queryset = queryset.filter(valor_total__lte=p['valor_max'])
        return queryset