from rest_framework import serializers

from api.serializers.get_or_none import serialize_instance
from db.models import ClientProfile, MyUser, StaffProfile, Order, OrderDetail


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'username',
            'is_active'
        ]


class MyUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'username',
            'password',
            'is_active'
        ]


class MyUserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = MyUser
        fields = [
            'username',
            'password',
            'is_active'
        ]


class ClientSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)

    class Meta:
        model = ClientProfile
        fields = '__all__'


class ClientCreateSerializer(ClientSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class ClientUpdateSerializer(ClientCreateSerializer):
    username = serializers.CharField(
        write_only=True,
        required=False
    )
    password = serializers.CharField(
        write_only=True,
        required=False
    )
    fullname = serializers.CharField(required=False)


class StaffSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)

    class Meta:
        model = StaffProfile
        fields = '__all__'


class StaffCreateSerializer(StaffSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class StaffUpdateSerializer(StaffCreateSerializer):
    username = serializers.CharField(
        write_only=True,
        required=False
    )
    password = serializers.CharField(
        write_only=True,
        required=False
    )
    fullname = serializers.CharField(required=False)
    role = serializers.IntegerField(required=False)


class OrderDetailSerializer(serializers.Serializer):
    color = serializers.CharField()
    size = serializers.CharField()
    amount = serializers.IntegerField()
    product_title = serializers.CharField()


class OrderClientSerializer(serializers.Serializer):
    id = serializers.CharField()
    fullname = serializers.CharField()


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    client_info = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_client_info(self, obj) -> OrderClientSerializer:
        return serialize_instance(
            obj.client,
            ["id", "fullname"]
        )

class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        details = validated_data.pop('details')
        instance = Order.objects.create(**validated_data)

        if details:
            create_data = []
            for d in details:
                create_data.append(
                    OrderDetail(
                        order=instance,
                        color=d['color'],
                        size=d['size'],
                        amount=d['amount'],
                        product_title=d['product_title']
                    )
                )

            OrderDetail.objects.bulk_create(create_data)

        return instance

    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        instance = super().update(instance, validated_data)

        if details:
            create_data = []
            for d in details:
                create_data.append(
                    OrderDetail(
                        order=instance,
                        color=d['color'],
                        size=d['size'],
                        amount=d['amount'],
                        product_title=d['product_title']
                    )
                )
            instance.details.all().delete()
            OrderDetail.objects.bulk_create(create_data)

        return instance








