import pytest


@pytest.mark.django_db
class TestSpecificModels:
    pass

    # def test_get_by_natural_key(self, geography_factory):
    #
    #     obj = geography_factory(level=1)
    #     result = Geography.objects.get_by_natural_key(obj.code_2)
    #     assert obj == result
