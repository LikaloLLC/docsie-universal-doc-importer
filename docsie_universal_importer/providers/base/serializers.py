from rest_framework import serializers
from swag_auth.models import ConnectorToken

from .fields import FileField


class BaseRequestSerializer(serializers.Serializer):
    token = serializers.PrimaryKeyRelatedField(queryset=ConnectorToken.objects.all())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['token'] = instance['token'].token

        return data


class StorageTreeRequestSerializer(BaseRequestSerializer):
    pass


class DownloaderRequestSerializer(BaseRequestSerializer):
    files = serializers.ListField(child=FileField())

    class Meta:
        file_cls = None

    def __init__(self, *args, **kwargs):
        if self.Meta.file_cls is None:
            raise AttributeError(f'`file_cls` must be given in {self.__module__}.{self.__class__.__name__}')

        super().__init__(*args, **kwargs)
