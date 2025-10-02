from rest_framework import serializers

from db.models import ClientProfile, MyUser, StaffProfile


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'is_active']


class MyUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'password', 'is_active']


class MyUserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'is_active']


class ClientSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)

    class Meta:
        model = ClientProfile
        fields = '__all__'


class ClientCreateSerializer(ClientSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class ClientUpdateSerializer(ClientCreateSerializer):
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
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
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    fullname = serializers.CharField(required=False)
    role = serializers.IntegerField(required=False)
