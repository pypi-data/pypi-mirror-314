from wbcore import serializers as wb_serializers

from .models import Geography


class GeographyRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:geography:geography-detail")
    _detail_preview = wb_serializers.HyperlinkField(reverse_name="wbcore:geography:geography-detail")

    class Meta:
        model = Geography
        fields = ["id", "representation", "_detail", "_detail_preview"]


class CountryRepresentationSerializer(GeographyRepresentationSerializer):
    filter_params = {"level": Geography.Level.COUNTRY.value}


class GeographyModelSerializer(wb_serializers.ModelSerializer):
    _parent = GeographyRepresentationSerializer(source="parent")

    class Meta:
        model = Geography
        fields = [
            "id",
            "name",
            "representation",
            "parent",
            "_parent",
            "code_2",
            "code_3",
        ]
