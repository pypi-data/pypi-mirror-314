from rest_framework import serializers

from .list import ListFieldMixin
from .mixins import WBCoreSerializerFieldMixin
from .types import WBCoreType


class ChoiceField(WBCoreSerializerFieldMixin, serializers.ChoiceField):
    field_type = WBCoreType.SELECT.value

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["choices"] = [{"value": k, "label": v} for k, v in self.choices.items()]
        return key, representation


class MultipleChoiceField(ListFieldMixin, WBCoreSerializerFieldMixin, serializers.MultipleChoiceField):
    field_type = WBCoreType.SELECT.value

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["multiple"] = True
        representation["choices"] = [{"value": k, "label": v} for k, v in self.choices.items()]
        return key, representation

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if isinstance(data, set):
            data = list(data)
        return data

    def to_representation(self, data):
        data = super().to_representation(data)
        if isinstance(data, set):
            data = list(data)
        return data
