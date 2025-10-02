from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from db.enums import UserStatus


# class UserLoginSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         token['status'] = user.status
#
#         return token

class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['status'] = self.user.status
        if self.user.status == UserStatus.STAFF:
            data['role'] = self.user.staff_profile.role

        return data