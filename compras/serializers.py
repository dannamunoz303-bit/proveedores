from rest_framework import serializers
from .models import Proveedor, Compra


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class CompraSerializer(serializers.ModelSerializer):
    # Solo lectura: muestra la información básica del proveedor
    proveedor_info = serializers.SerializerMethodField()

    class Meta:
        model = Compra
        fields = '__all__'

    def get_proveedor_info(self, obj):
        return {
            'id': obj.proveedor.id,
            'nombre': obj.proveedor.nombre,
        }