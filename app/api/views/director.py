from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsDirector
from api.serializers.director import ClientSerializer, ClientCreateSerializer, ClientUpdateSerializer, \
    MyUserCreateSerializer, MyUserUpdateSerializer, StaffSerializer, StaffCreateSerializer, StaffUpdateSerializer
from db.enums import UserStatus
from db.models import ClientProfile, MyUser, StaffProfile


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


