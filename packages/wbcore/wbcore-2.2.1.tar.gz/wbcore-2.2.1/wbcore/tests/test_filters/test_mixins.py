from unittest.mock import patch

import pytest
from faker import Faker
from rest_framework.viewsets import ViewSet
from wbcore.filters.fields import CharFilter

fake = Faker()


class TestWBCoreFilterMixin:
    @pytest.fixture()
    def view(self):
        return ViewSet()

    @pytest.mark.parametrize("field_name", [fake.word()])
    def test_key_column_name(self, field_name):
        filter_field = CharFilter(column_field_name=field_name, field_name=field_name)
        assert filter_field.key == field_name

    @pytest.mark.parametrize("field_name", [fake.word()])
    def test_key_field_name(self, field_name):
        filter_field = CharFilter(field_name=field_name)
        assert filter_field.key == field_name

    @pytest.mark.parametrize("label", [fake.word()])
    def test_get_label_with_label(self, label):
        filter_field = CharFilter(label=label)
        assert filter_field.get_label() == label

    @pytest.mark.parametrize("field_name1, field_name2", [(fake.word(), fake.word())])
    def test_get_label_without_label(self, field_name1, field_name2):
        field_name = field_name1 + "_" + field_name2
        filter_field = CharFilter(field_name=field_name)
        assert filter_field.get_label() == field_name1.title() + " " + field_name2.title()

    @pytest.mark.parametrize("default", [fake.word()])
    def test__get_default_with_callable(self, rf, default, view):
        filter_field = CharFilter(default=lambda f, r, v: default)
        assert filter_field._get_default(rf, view) == default

    @pytest.mark.parametrize("default", [fake.word()])
    def test__get_default_with_callable_str(self, rf, default, view):
        class CustomFilterField(CharFilter):
            def custom_default(self, *args):
                return default

        filter_field = CustomFilterField(default="custom_default")
        assert filter_field._get_default(rf, view) == default

    @pytest.mark.parametrize("default", [fake.word()])
    def test__get_default_with_default(self, rf, default, view):
        filter_field = CharFilter(default=default)
        assert filter_field._get_default(rf, view) == default

    @pytest.mark.parametrize("name", [fake.word()])
    def test_get_representation(self, name, rf, view):
        filter_field = CharFilter(field_name=name)
        request = rf.get("")
        rep, _ = filter_field.get_representation(request, name, view)
        for key in ["label", "key", "label_format"]:
            assert key in rep

    @pytest.mark.parametrize("name, initial", [(fake.word(), fake.word())])
    def test_get_representation_request_initial(self, name, initial, rf, view):
        filter_field = CharFilter(field_name=name)
        rf.GET = {name: initial}
        _, le = filter_field.get_representation(rf, name, view)
        assert le["input_properties"]["initial"] == initial

    @pytest.mark.parametrize("name, default", [(fake.word(), fake.word())])
    def test_get_representation_field_default(self, name, default, rf, view):
        filter_field = CharFilter(field_name=name, default=default)
        request = rf.get("")
        _, le = filter_field.get_representation(request, name, view)
        assert le["input_properties"]["default"] == default

    @pytest.mark.parametrize("name, default, help_text", [(fake.word(), fake.word(), fake.word())])
    def test_get_help_text(self, name, default, help_text, rf, view):
        request = rf.get("")

        # assert that no field nor help text nor label returns an empty help_text
        filter_field = CharFilter(field_name=name, default=default, help_text=None)
        assert filter_field.get_representation(request, name, view)[0]["help_text"] is None

        # assert that no field nor help text but a label returns an "Filter by {{label}}"
        filter_field = CharFilter(field_name=name, default=default, help_text=None, label=help_text)
        assert filter_field.get_representation(request, name, view)[0]["help_text"] == f"Filter by {help_text}"

        filter_field = CharFilter(field_name=name, default=default, help_text=help_text)
        assert filter_field.get_representation(request, name, view)[0]["help_text"] == help_text

    @patch("wbcore.filters.mixins.get_model_field")
    @pytest.mark.parametrize("name, default, text", [(fake.word(), fake.word(), fake.word())])
    def test_get_help_text_from_model_help_text(self, mock_fct, name, default, text, rf, view):
        class Field:
            help_text = text

        class dummy_parent:
            class _meta:
                model = "tmp"

        mock_fct.return_value = Field

        filter_field = CharFilter(field_name=name, default=default, help_text=None)
        filter_field.parent = dummy_parent()
        request = rf.get("")
        assert filter_field.get_representation(request, name, view)[0]["help_text"] == text
