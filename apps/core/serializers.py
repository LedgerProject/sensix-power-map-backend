from rest_framework import serializers


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
