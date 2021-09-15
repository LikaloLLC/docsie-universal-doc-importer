import os.path
from dataclasses import _MISSING_TYPE

from rest_framework import serializers

from docsie_universal_importer import app_settings


class FileField(serializers.DictField):
    default_error_messages = {
        'required_key_missing': 'Required field `{field}` missing.',
        'extension_not_allowed': 'Extension `{extension}` not allowed. Must be one of {allowed_extensions}',
    }

    def to_internal_value(self, file):
        parent_serializer = self.parent.parent
        from_file_cls = parent_serializer.Meta.file_cls

        for field_name, field in from_file_cls.__dataclass_fields__.items():
            if isinstance(field.default, _MISSING_TYPE) and field.init and field_name not in file:
                self.fail('required_key_missing', field=field_name)

        extension = os.path.splitext(file['name'])[1][1:]
        allowed_extensions = app_settings.ALLOWED_EXTENSIONS

        if allowed_extensions != '*' and extension not in allowed_extensions:
            self.fail('extension_not_allowed', extension=extension, allowed_extensions=allowed_extensions)

        return super().to_internal_value(file)
