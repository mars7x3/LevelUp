from rest_framework import serializers

from db.models import ProductCode


class OTKWorkSerializer(serializers.Serializer):
    internal_code = serializers.CharField()
    comment = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    is_defect = serializers.BooleanField(default=False)


class PackerWorkSerializer(serializers.Serializer):
    internal_code = serializers.CharField()


class MarkerWorkSerializer(serializers.Serializer):
    internal_code = serializers.CharField()


class MarkerFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = ['file']
