from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsDirector
from api.serializers.director import ClientSerializer, ClientCreateSerializer, ClientUpdateSerializer, \
    MyUserCreateSerializer, MyUserUpdateSerializer, StaffSerializer, StaffCreateSerializer, StaffUpdateSerializer, \
    OrderSerializer, OrderCreateUpdateSerializer, StatementSerializer, StatementUpdateSerializer

from db.enums import UserStatus, StatementType, ProductStatus
from db.models import ClientProfile, MyUser, StaffProfile, Order, Statement, Product, Work


class ClientModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDirector]
    queryset = ClientProfile.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientSerializer
        elif self.request.method == 'POST':
            return ClientCreateSerializer
        else:
            return ClientUpdateSerializer

    @extend_schema(
        request=ClientCreateSerializer,
        responses=ClientSerializer
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = {
            'username': serializer.validated_data.pop('username'),
            'password': serializer.validated_data.pop('password'),
            'status': UserStatus.CLIENT
        }
        user_serializer = MyUserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = MyUser.objects.create_user(**user_data)

        client_profile = ClientProfile.objects.create(
            user=user,
            **serializer.validated_data
        )
        serializer = ClientSerializer(
            client_profile,
            context=self.get_renderer_context()
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(request=ClientUpdateSerializer, responses=ClientSerializer)
    def update(self, request, *args, **kwargs):
        client_profile = self.get_object()
        serializer = self.get_serializer(client_profile, data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = {}
        if serializer.validated_data.get('username'):
            user_data['username'] = serializer.validated_data.get('username')
        if serializer.validated_data.get('password'):
            user_data['password'] = serializer.validated_data.pop('password')

        if user_data:
            user_serializer = MyUserUpdateSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.update(client_profile.user, user_serializer.data)
            user.set_password(user_data.get('password'))
            user.save()

        self.perform_update(serializer)
        serializer = ClientSerializer(client_profile, context=self.get_renderer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ClientUpdateSerializer, responses=ClientSerializer)
    def partial_update(self, request, *args, **kwargs):
        client_profile = self.get_object()
        serializer = self.get_serializer(client_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user_data = {}
        if serializer.validated_data.get('username'):
            user_data['username'] = serializer.validated_data.get('username')
        if serializer.validated_data.get('password'):
            user_data['password'] = serializer.validated_data.pop('password')

        if user_data:
            user_serializer = MyUserUpdateSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.update(client_profile.user, user_serializer.data)
            user.set_password(user_data.get('password'))
            user.save()

        self.perform_update(serializer)
        serializer = ClientSerializer(client_profile, context=self.get_renderer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        client_profile = self.get_object()
        user = client_profile.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDirector]
    queryset = StaffProfile.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StaffSerializer
        elif self.request.method == 'POST':
            return StaffCreateSerializer
        else:
            return StaffUpdateSerializer

    @extend_schema(
        request=StaffCreateSerializer,
        responses=StaffSerializer
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = {
            'username': serializer.validated_data.pop('username'),
            'password': serializer.validated_data.pop('password'),
            'status': UserStatus.STAFF
        }
        user_serializer = MyUserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = MyUser.objects.create_user(**user_data)

        staff_profile = StaffProfile.objects.create(
            user=user,
            **serializer.validated_data
        )
        serializer = StaffSerializer(
            staff_profile,
            context=self.get_renderer_context()
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(request=StaffUpdateSerializer, responses=StaffSerializer)
    def update(self, request, *args, **kwargs):
        staff_profile = self.get_object()
        serializer = self.get_serializer(staff_profile, data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = {}
        if serializer.validated_data.get('username'):
            user_data['username'] = serializer.validated_data.get('username')
        if serializer.validated_data.get('password'):
            user_data['password'] = serializer.validated_data.pop('password')

        if user_data:
            user_serializer = MyUserUpdateSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.update(staff_profile.user, user_serializer.data)
            user.set_password(user_data.get('password'))
            user.save()

        self.perform_update(serializer)
        serializer = StaffSerializer(staff_profile, context=self.get_renderer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=StaffUpdateSerializer, responses=StaffSerializer)
    def partial_update(self, request, *args, **kwargs):
        staff_profile = self.get_object()
        serializer = self.get_serializer(staff_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user_data = {}
        if serializer.validated_data.get('username'):
            user_data['username'] = serializer.validated_data.get('username')
        if serializer.validated_data.get('password'):
            user_data['password'] = serializer.validated_data.pop('password')

        if user_data:
            user_serializer = MyUserUpdateSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.update(staff_profile.user, user_serializer.data)
            user.set_password(user_data.get('password'))
            user.save()

        self.perform_update(serializer)
        serializer = StaffSerializer(staff_profile, context=self.get_renderer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        staff_profile = self.get_object()
        user = staff_profile.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderModelViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated, IsDirector]
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer


class OrderReadViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsDirector]
    queryset = Order.objects.select_related('client').prefetch_related('order_products__details')
    serializer_class = OrderSerializer


class StatementListView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Statement.objects.filter(
        type=StatementType.CODE,
        is_moderated=False
    ).select_related('product', 'staff')
    serializer_class = StatementSerializer


class UpdateStatementView(APIView):
    permission_classes = [IsAuthenticated, IsDirector]

    @extend_schema(request=StatementUpdateSerializer())
    def post(self, request):
        serializer = StatementUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        statement = Statement.objects.filter(
            id=validated['statement_id'],
            is_moderated=False
        ).first()

        if statement:
            if validated.get('is_success'):
                product = statement.product

                Work.objects.filter(
                    product=product,
                    status=ProductStatus.MARKER

                ).delete()

                product.status = ProductStatus.PACKER
                product.save()

            statement.is_moderated = True
            statement.save()

            return Response('OK!')

        return Response(
            'Заявка уже прошла модерацию!',
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderDetailView(APIView):
    def get(self, request):
        order_id = request.query_params.get('order_id')
        order = (
            Order.objects
            .filter(id=order_id)
            .prefetch_related(
                'order_products__details',
                'products__works__staff'
            )
            .first()
        )

        if not order:
            return Response({'error': 'Order not found'}, status=404)

        # === 1. СВОДКА ПО ВСЕМ ПРОДУКТАМ ===
        summary = dict(
            order.products
            .values('status')
            .annotate(total=Count('id'))
            .values_list('status', 'total')
        )

        summary = {
            status.name: summary.get(status.value, 0)
            for status in ProductStatus
        }

        # === 2. Детализация по каждому OrderProduct ===
        info = []

        for op in order.order_products.all():
            planned_total = sum(d.amount for d in op.details.all())

            # Все продукты для этого order_product (по совпадению названия)
            related_products = order.products.filter(title=op.product_title)

            # Факт по статусу RECEIVER
            fact_total = related_products.filter(
                works__status=ProductStatus.RECEIVER
            ).distinct().count()

            details_list = []
            for d in op.details.all():
                # fact_amount: сколько изделий этого цвета и размера прошли RECEIVER
                fact_amount = related_products.filter(
                    color=d.color,
                    size=d.size,
                    works__status=ProductStatus.RECEIVER
                ).distinct().count()

                # группируем работы по статусу и сотрудникам
                works_data = []
                works_qs = (
                    related_products
                    .filter(color=d.color, size=d.size)
                    .values(
                        'works__status',
                        'works__staff__fullname'
                    )
                    .annotate(amount=Count('works__id'))
                )

                # группировка по статусу
                status_groups = {}
                for w in works_qs:
                    st = w['works__status']
                    status_groups.setdefault(st, {})
                    status_groups[st][w['works__staff__fullname']] = w['amount']

                for st, staffs in status_groups.items():
                    works_data.append({
                        'status': st,
                        'amount': sum(staffs.values()),
                        'staffs': [
                            {'fullname': name, 'amount': cnt}
                            for name, cnt in staffs.items()
                        ]
                    })

                details_list.append({
                    'color': d.color,
                    'size': d.size,
                    'planned_amount': d.amount,
                    'fact_amount': fact_amount,
                    'works': works_data
                })

            info.append({
                'product_title': op.product_title,
                'planned_total': planned_total,
                'fact_total': fact_total,
                'details': details_list
            })

        # === 3. Формируем итог ===
        result = {
            'summary': summary,
            'info': info
        }

        return Response(result)



