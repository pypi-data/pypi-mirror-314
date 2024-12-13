import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory
from termcolor import colored
from wbcore.contrib.directory.factories import PersonFactory
from wbcore.contrib.directory.typings import Person as PersonDTO
from wbcore.contrib.directory.viewsets import UserIsManagerViewSet
from wbcore.test import GenerateTest, default_config
from wbcore.test.mixins import TestViewSet
from wbcore.test.utils import get_data_from_factory, get_kwargs, get_or_create_superuser

config = {}
for key, value in default_config.items():
    config[key] = list(
        filter(
            lambda x: x.__module__.startswith("wbcore.contrib.directory")
            and x.__name__
            not in [
                "UserIsManagerViewSet",
                "UserIsClientViewSet",
                "ActivityParticipantModelViewSet",
                "ClientManagerViewSet",
            ],
            value,
        )
    )


@pytest.mark.django_db
@GenerateTest(config)
class TestProject:
    pass


# UserIsManagerViewSet Test
class CustomTestViewSet(TestViewSet):
    def test_post_endpoint(self, client):
        pass


class GenerateUserIsManagerTest(GenerateTest):
    def test_modelviewsets(_self, mvs, client):
        my_test = CustomTestViewSet(mvs)
        my_test.execute_test_list_endpoint(client)
        my_test.execute_test_detail_endpoint()


@pytest.mark.django_db
@GenerateUserIsManagerTest({"viewsets": [UserIsManagerViewSet]})
class TestUserIsManager:
    @pytest.mark.parametrize("mvs", config.get("viewsets", []))
    def test_something_specific(_self, mvs):
        assert True


# ActivityParticipantModelViewSet Test
class ActivityParticipantTestViewSet(TestViewSet):
    def _get_mixins_update_data(self, type):
        api_request = APIRequestFactory()
        superuser = get_or_create_superuser()
        obj = self.factory()
        data = get_data_from_factory(obj, self.mvs, superuser=superuser, update=True)
        data["participant"] = PersonFactory().id
        if type == "PATCH":
            request = api_request.patch("", data)
        else:  # "UPDATE"
            request = api_request.put("", data)
        request.user = superuser
        kwargs = get_kwargs(obj, self.mvs, request=request, data=data)
        return obj, request, kwargs, data

    def test_patch_request(self):
        obj, request, kwargs, data = self._get_mixins_update_data("PATCH")
        vs = self.mvs.as_view({"patch": "partial_update"})
        ep = self._get_endpoint_config(request, kwargs, obj)
        ep_update = ep.get_instance_endpoint()
        response = vs(request, **kwargs, data=data)
        if ep_update:
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
        else:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
                str(response.status_code) + f" == 405 ({response.data})"
            )
        print(f"- {self.__class__.__name__}:test_patchviewset", colored("PASSED", "green"))  # noqa: T201

    def test_update_request(self):
        obj, request, kwargs, _ = self._get_mixins_update_data("UPDATE")
        vs = self.mvs.as_view({"put": "update"})
        ep = self._get_endpoint_config(request, kwargs, obj)
        ep_update = ep.get_instance_endpoint()
        response = vs(request, **kwargs)
        if ep_update:
            assert response.status_code == status.HTTP_200_OK, str(response.status_code) + f" == 200 ({response.data})"
            assert response.data.get("instance"), str(response.data.get("instance")) + " should not be empty"
        else:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
                str(response.status_code) + f" == 405 ({response.data})"
            )
        print(f"- {self.__class__.__name__}:test_update_request", colored("PASSED", "green"))  # noqa: T201


class GenerateActivityParticipantTest(GenerateTest):
    def test_modelviewsets(_self, mvs, client):
        my_test = ActivityParticipantTestViewSet(mvs)
        my_test.execute_test_list_endpoint(client)
        my_test.execute_test_detail_endpoint()


@pytest.mark.django_db
class TestDTO:
    @pytest.mark.parametrize(
        "id, name, email",
        [
            (None, None, None),
            (None, "test", None),
            (None, "test", "test@test.com"),
            (1, None, None),
            (1, "test", None),
            (1, "test", "test@test.com"),
        ],
    )
    def test_comparison(self, id, name, email):
        person1 = PersonDTO(1, "test", "test", "test@test.com")
        person2 = PersonDTO(id=id, first_name=name, last_name=name, email=email)
        if (person1.id == person2.id is not None) or (person1.email == person2.email is not None):
            assert person1 == person2
        else:
            assert person1 != person2
        assert person2 is not None
