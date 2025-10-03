from rest_framework import serializers


class OTKWorkSerializer(serializers.Serializer):
    internal_code = serializers.CharField()
    comment = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    is_defect = serializers.BooleanField(default=False)


class PackerWorkSerializer(serializers.Serializer):
    internal_code = serializers.CharField()
