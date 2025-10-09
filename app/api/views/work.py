from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOTK, IsPacker, IsMarker
from api.serializers.work import OTKWorkSerializer, PackerWorkSerializer, MarkerFilesSerializer, MarkerWorkSerializer
from db.enums import ProductStatus, CodeType, StatementType
from db.models import Product, Work, WorkImage, Statement


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
        if product:

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
            return Response(
                'Повторно провести не получится!',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Товар не сущестует!',
            status=status.HTTP_400_BAD_REQUEST
        )


class PackerWorkView(APIView):
    permission_classes = [IsAuthenticated, IsPacker]

    @extend_schema(request=PackerWorkSerializer())
    def post(self, request):
        serializer = PackerWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        product = Product.objects.filter(internal_code=validated['internal_code']).first()
        if product:

            if product.status in [
                ProductStatus.RECEIVER,
                ProductStatus.OTK
            ]:
                product.status = ProductStatus.PACKER
                product.save()

                Work.objects.create(
                    product=product,
                    staff=request.user.staff_profile,
                    status=product.status,
                )

                return Response('OK!')
            return Response(
                'Повторно провести не получится!',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Товар не сущестует!',
            status=status.HTTP_400_BAD_REQUEST
        )

class MarkerImagesView(APIView):
    permission_classes = [IsAuthenticated, IsMarker]

    @extend_schema(
        responses=MarkerFilesSerializer(many=True)
    )
    def get(self, request):
        internal_code = request.query_params.get('internal_code')

        product = Product.objects.filter(internal_code=internal_code).first()
        if product:

            if product.status in [
                ProductStatus.RECEIVER,
                ProductStatus.PACKER
            ]:
                codes = product.codes.exclude(type=CodeType.INTERNAL)

                serializer = MarkerFilesSerializer(
                    codes,
                    many=True,
                    context=self.get_renderer_context()
                )
                return Response(serializer.data)
            return Response(
                'Повторно провести не получится!',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Товар не сущестует!',
            status=status.HTTP_400_BAD_REQUEST
        )

class MarkerWorkView(APIView):
    permission_classes = [IsAuthenticated, IsMarker]

    @extend_schema(request=MarkerWorkSerializer())
    def post(self, request):
        serializer = MarkerWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        product = Product.objects.filter(internal_code=validated['internal_code']).first()
        if product:

            if product.status in [
                ProductStatus.RECEIVER,
                ProductStatus.PACKER
            ]:
                hs = product.codes.filter(type=CodeType.HS).first()
                product.status = ProductStatus.MARKER
                product.internal_code = hs.code if hs else product.internal_code
                product.save()

                Work.objects.create(
                    product=product,
                    staff=request.user.staff_profile,
                    status=product.status,
                )

                return Response('OK!')
            return Response(
                'Повторно провести не получится!',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Товар не сущестует!',
            status=status.HTTP_400_BAD_REQUEST
        )


class CreateStatementView(APIView):
    permission_classes = [IsAuthenticated, IsMarker]

    @extend_schema(request=MarkerWorkSerializer())
    def post(self, request):
        serializer = MarkerWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        product = Product.objects.filter(internal_code=validated['internal_code']).first()
        if product:
            statement, created = Statement.objects.get_or_create(
                product=product,
                type=StatementType.CODE,
                is_moderated=False,
                staff=request.user.staff_profile
            )
            if created:
                return Response('OK!')

            return Response(
            'Заявка уже сущестует!',
            status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Товар не сущестует!',
            status=status.HTTP_400_BAD_REQUEST
        )