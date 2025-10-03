from django.template.defaulttags import comment
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOTK, IsPacker
from api.serializers.work import OTKWorkSerializer, PackerWorkSerializer
from db.enums import ProductStatus
from db.models import Product, Work, WorkImage


class OTKWorkView(APIView):
    permission_classes = [IsAuthenticated, IsOTK]

    @extend_schema(request=OTKWorkSerializer())
    def post(self, request):
        serializer = OTKWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        if validated.get('is_defect'):
            prod_status = ProductStatus.DEFECT
        else:
            prod_status = ProductStatus.OTK

        product = Product.objects.filter(internal_code=validated['internal_code']).first()

        if product.status == ProductStatus.RECEIVER:

            product.status = prod_status
            product.save()

            work = Work.objects.create(
                product=product,
                staff=request.user.staff_profile,
                status=prod_status,
                comment=validated.get('comment')
            )

            if validated.get('is_defect'):
                WorkImage.objects.create(
                    work=work,
                    image=validated.get('image')
                )

            return Response('OK!')
        return Response('Повторно провести не получится!', status=status.HTTP_400_BAD_REQUEST)


class PackerWorkView(APIView):
    permission_classes = [IsAuthenticated, ]

    @extend_schema(request=PackerWorkSerializer())
    def post(self, request):
        serializer = PackerWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        product = Product.objects.filter(internal_code=validated['internal_code']).first()

        if product.status in [ProductStatus.RECEIVER, ProductStatus.OTK]:
            product.status = ProductStatus.PACKER
            product.save()

            Work.objects.create(
                product=product,
                staff=request.user.staff_profile,
                status=ProductStatus.PACKER,
            )

            return Response('OK!')
        return Response('Повторно провести не получится!', status=status.HTTP_400_BAD_REQUEST)


