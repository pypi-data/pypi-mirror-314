from wbcore import serializers

from .models import ReleaseNote


class ReleaseNoteModelSerializer(serializers.ModelSerializer):
    user_read = serializers.BooleanField()

    class Meta:
        model = ReleaseNote
        fields = (
            "id",
            "version",
            "release_date",
            "module",
            "summary",
            "notes",
            "user_read",
        )
