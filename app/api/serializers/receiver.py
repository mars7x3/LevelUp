from rest_framework import serializers

from api.serializers.get_or_none import serialize_instance
from db.models import Order


class OrderClientSerializer(serializers.Serializer):
    id = serializers.CharField()
    fullname = serializers.CharField()


class OrderDetailAmountSerializer(serializers.Serializer):
    color = serializers.CharField()
    size = serializers.CharField()
    amount = serializers.IntegerField()


class OrderProductsSerializer(serializers.Serializer):
    product_title = serializers.CharField()
    details = OrderDetailAmountSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    client_info = serializers.SerializerMethodField()
    order_products = OrderProductsSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'created_at',
            'client_info',
            'order_products'
        ]

    def get_client_info(self, obj) -> OrderClientSerializer:
        return serialize_instance(
            obj.client,
            ["id", "fullname"]
        )


class CreateProductSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    title = serializers.CharField()
    color = serializers.CharField()
    size = serializers.CharField()
    internal_code = serializers.CharField()
    file = serializers.FileField()