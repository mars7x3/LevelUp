from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsReceiver
from api.serializers.receiver import OrderSerializer, CreateProductSerializer
from db.enums import OrderStatus, CodeType, ProductStatus
from db.models import Order, Product, ProductCode


class OrderListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsReceiver]
    queryset = Order.objects.filter(
        status=OrderStatus.PROGRES
    ).select_related('client').prefetch_related('order_products')
    serializer_class = OrderSerializer


class ReceptionView(APIView):
    permission_classes = [IsAuthenticated, IsReceiver]

    @extend_schema(request=CreateProductSerializer())
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        product = Product.objects.create(
            order_id=validated['order_id'],
            title=validated["title"],
            color=validated["color"],
            size=validated["size"],
            internal_code=validated["internal_code"],
            status=ProductStatus.RECEIVER
        )
        ProductCode.objects.create(
            product=product,
            file=validated["file"],
            code=validated["internal_code"],
            type=CodeType.INTERNAL
        )

        return Response('OK!')
