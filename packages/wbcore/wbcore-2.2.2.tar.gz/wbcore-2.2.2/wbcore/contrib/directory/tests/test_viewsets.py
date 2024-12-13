import json

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory
from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.directory.models import ClientManagerRelationship as CMR
from wbcore.contrib.directory.models import Person
from wbcore.test.utils import (
    get_data_from_factory,
    get_kwargs,
    get_model_factory,
    get_or_create_superuser,
)

from ..factories import ClientManagerRelationshipFactory, EntryFactory, PersonFactory
from ..viewsets import (
    AddressContactEntryViewSet,
    BankingContactEntryViewSet,
    ClientManagerViewSet,
    CompanyModelViewSet,
    CompanyRepresentationViewSet,
    CompanyTypeModelViewSet,
    CustomerStatusModelViewSet,
    EmailContactEntryViewSet,
    EntryRepresentationViewSet,
    PersonRepresentationViewSet,
    PositionModelViewSet,
    RelationshipModelViewSet,
    RelationshipTypeModelViewSet,
    SocialMediaContactEntryViewSet,
    SpecializationModelViewSet,
    TelephoneContactEntryViewSet,
    UserIsClientViewSet,
    UserIsManagerViewSet,
    WebsiteContactEntryViewSet,
)


@pytest.mark.django_db
class TestEntryModelViewSet:
    api_factory = APIRequestFactory()

    @pytest.mark.parametrize(
        "rmvs",
        [
            EntryRepresentationViewSet,
            PersonRepresentationViewSet,
            CompanyRepresentationViewSet,
        ],
    )
    def test_get_queryset(self, rmvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=False)
        factory = get_model_factory(rmvs.queryset.model)
        obj = factory()
        kwargs = get_kwargs(obj, rmvs, request)
        vs = rmvs.as_view({"get": "list"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("rmvs", [CompanyRepresentationViewSet])
    def test_get_queryset_CompanyRepresentationViewSet(self, rmvs, company_factory):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=False)
        request.user.profile.employers.add(company_factory())
        factory = get_model_factory(rmvs.queryset.model)
        obj = factory()
        kwargs = get_kwargs(obj, rmvs, request)
        vs = rmvs.as_view({"get": "list"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("mvs", [CompanyModelViewSet])
    def test_get_company_instance(self, mvs, company_factory):
        # Arrange
        company = company_factory()
        request = self.api_factory.get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        view = mvs.as_view({"get": "retrieve"})
        # Act
        response = view(request, pk=company.id).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.data["instance"]["id"] == company.id

    @pytest.mark.parametrize("mvs", [CompanyModelViewSet])
    def test_get_company_list(self, mvs, company_factory):
        # Arrange
        company_factory.create_batch(3)
        request = self.api_factory.get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        view = mvs.as_view({"get": "list"})
        # Act
        response = view(request).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert not response.data.get("instance")
        assert response.data.get("results")
        assert response.data["results"]
        assert len(response.data["results"]) == 3

    @pytest.mark.parametrize("mvs", [CompanyModelViewSet])
    def test_delete_company_instance(self, mvs, company_factory):
        # Arrange
        company = company_factory()
        request = self.api_factory.delete("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        view = mvs.as_view({"delete": "destroy"})
        # Act
        response = view(request, pk=company.id).render()
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize(
        "mvs",
        [
            EmailContactEntryViewSet,
            AddressContactEntryViewSet,
            TelephoneContactEntryViewSet,
            WebsiteContactEntryViewSet,
            BankingContactEntryViewSet,
        ],
    )
    def test_post_delete_contact(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        factory(entry=obj.entry)
        user = get_or_create_superuser()
        data = get_data_from_factory(obj, mvs, delete=True, superuser=user)
        request = APIRequestFactory().post("", data)
        request.user = user
        kwargs = get_kwargs(obj, mvs, request=request, data=data)
        vs = mvs.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("instance")


# # =====================================================================================================================
# #                                                  TESTING UTILS VIEWSETS
# # =====================================================================================================================


@pytest.mark.django_db
class TestUtilsViewSets:
    api_factory = APIRequestFactory()

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_get_utils(self, mvs):
        request = self.api_factory.get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        factory = get_model_factory(mvs.queryset.model)
        factory.create_batch(3)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 3
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_retrieve_utils(self, mvs):
        request = self.api_factory.get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.id)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_post_utils(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        super_user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(obj, mvs, superuser=super_user, delete=True)
        request = self.api_factory.post("", data=data)
        request.user = super_user
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_delete_utils(self, mvs):
        request = self.api_factory.delete("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"delete": "destroy"})
        response = vs(request, **kwargs, pk=obj.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_put_utils(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        old_obj = factory()
        new_obj = factory()
        user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(new_obj, mvs, superuser=user, delete=True)
        request = APIRequestFactory().put("", data=data)
        request.user = user
        vs = mvs.as_view({"put": "update"})
        response = vs(request, pk=old_obj.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == new_obj.title
        assert not response.data["instance"]["title"] == old_obj.title

    @pytest.mark.parametrize(
        "mvs",
        [
            CustomerStatusModelViewSet,
            PositionModelViewSet,
            CompanyTypeModelViewSet,
            SpecializationModelViewSet,
        ],
    )
    def test_patch_utils(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        request = APIRequestFactory().patch("", data={"title": "New Title"})
        request.user = UserFactory(is_active=True, is_superuser=True)
        vs = mvs.as_view({"patch": "partial_update"})
        response = vs(request, pk=obj.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == "New Title"


# =====================================================================================================================
#                                                  TESTING RELATIONSHIP VIEWSETS
# =====================================================================================================================


@pytest.mark.django_db
class TestRelationshipViewSets:
    api_factory = APIRequestFactory()

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_retrieve(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        factory = get_model_factory(mvs.queryset.model)
        type = factory()
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=type.id)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_get(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        factory = get_model_factory(mvs.queryset.model)
        factory.create_batch(3)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 6
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_put(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        old_type = factory()
        non_counter_type = factory(counter_relationship=None)
        new_type = factory()
        new_type.counter_relationship = non_counter_type
        user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(new_type, mvs, superuser=user, delete=True)
        request = APIRequestFactory().put("", data=data)
        request.user = user
        vs = mvs.as_view({"put": "update"})
        response = vs(request, pk=old_type.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == new_type.title
        assert not response.data["instance"]["title"] == old_type.title
        assert response.data["instance"]["counter_relationship"] == new_type.counter_relationship.id

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_delete(self, mvs):
        request = APIRequestFactory().delete("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        factory = get_model_factory(mvs.queryset.model)
        type = factory()
        vs = mvs.as_view({"delete": "destroy"})
        response = vs(request, pk=type.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_patch(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        type = factory()
        request = APIRequestFactory().patch("", data={"title": "New Title"})
        request.user = UserFactory(is_active=True, is_superuser=True)
        vs = mvs.as_view({"patch": "partial_update"})
        response = vs(request, pk=type.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == "New Title"

    @pytest.mark.parametrize("mvs", [RelationshipTypeModelViewSet])
    def test_relationshiptype_post(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        type = factory(counter_relationship=None)
        user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(type, mvs, superuser=user, delete=True)
        json_data = json.dumps(data)
        request = APIRequestFactory().post("", data=json_data, content_type="application/json")
        request.user = user
        kwargs = get_kwargs(type, mvs, request)
        vs = mvs.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED

    def test_relationship_list(self, relationship_factory, relationship_type_factory):
        # Arrange
        relationship_type = relationship_type_factory(counter_relationship=None)
        request = self.api_factory.get("")
        request.user = UserFactory(is_active=True, is_superuser=True)

        relationship_factory.create_batch(3, relationship_type=relationship_type)
        view = RelationshipModelViewSet.as_view({"get": "list"})
        # Act
        response = view(request).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("results")
        assert len(response.data["results"]) == 3 * 2

    def test_relationship_retrieve(self, relationship_factory):
        # Arrange
        relationship = relationship_factory()
        request = self.api_factory.get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        view = RelationshipModelViewSet.as_view({"get": "retrieve"})
        # Act
        response = view(request, pk=relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)["instance"]["from_entry"] == relationship.from_entry.id
        assert json.loads(response.content)["instance"]["to_entry"] == relationship.to_entry.id
        assert json.loads(response.content)["instance"]["relationship_type"] == relationship.relationship_type.id

    def test_relationship_delete(self, relationship_factory):
        # Arrange
        relationship = relationship_factory()
        request = self.api_factory.delete("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        view = RelationshipModelViewSet.as_view({"delete": "destroy"})
        # Act
        response = view(request, pk=relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_relationship_create(self, relationship_factory):
        # Arrange
        relationship = relationship_factory()
        user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(relationship, RelationshipModelViewSet, superuser=user)
        request = self.api_factory.post("", data=data)
        request.user = user
        kwargs = get_kwargs(relationship, RelationshipModelViewSet, request=request, data=data)
        view = RelationshipModelViewSet.as_view({"post": "create"})
        # Act
        response = view(request, kwargs).render()
        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_relationship_update(self, relationship_factory):
        # Arrange
        old_relationship = relationship_factory()
        new_relationship = relationship_factory()
        user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(new_relationship, RelationshipModelViewSet, superuser=user)
        request = self.api_factory.put("", data=data)
        request.user = user
        view = RelationshipModelViewSet.as_view({"put": "update"})
        # Act
        response = view(request, pk=old_relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_relationship_partial_update(self, relationship_factory, person_factory):
        # Arrange
        relationship = relationship_factory()
        new_Person = person_factory()
        request = self.api_factory.patch("", data={"to_entry": new_Person.id})
        request.user = UserFactory(is_active=True, is_superuser=True)
        view = RelationshipModelViewSet.as_view({"patch": "partial_update"})
        # Act
        response = view(request, pk=relationship.id).render()
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["to_entry"] == new_Person.id


# =====================================================================================================================
#                                                  TESTING CLIENT MANAGER VIEWSETS
# =====================================================================================================================


@pytest.mark.django_db
class TestClientManagerViewSet:
    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_None_qs(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=False)
        obj = ClientManagerRelationshipFactory()
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"get": "list"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_delete(self, mvs):
        request = APIRequestFactory().delete("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        obj1 = ClientManagerRelationshipFactory()
        obj2 = ClientManagerRelationshipFactory(client=obj1.client, status=CMR.Status.DRAFT)
        view = mvs.as_view({"delete": "destroy"})
        response = view(request, pk=obj2.id).render()
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_get(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        ClientManagerRelationshipFactory.create_batch(3)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 3
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_retrieve(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        obj = ClientManagerRelationshipFactory()
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.pk)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_put(self, mvs):
        obj_old = ClientManagerRelationshipFactory(status=CMR.Status.DRAFT)
        obj_new = ClientManagerRelationshipFactory()
        user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(obj_new, mvs, superuser=user, delete=True)
        request = APIRequestFactory().put("", data=data)
        request.user = user
        kwargs = get_kwargs(obj_old, mvs, request, data)
        vs = mvs.as_view({"put": "update"})
        response = vs(request, pk=obj_old.id, **kwargs).render()
        assert response.status_code == status.HTTP_200_OK
        assert not obj_old.client == obj_new.client
        assert response.data["instance"]["id"] == obj_old.id
        assert response.data["instance"]["client"] == obj_new.client.id
        assert not response.data["instance"]["client"] == obj_old.client.id

    @pytest.mark.parametrize("mvs", [ClientManagerViewSet])
    def test_post(self, mvs):
        cmr = ClientManagerRelationshipFactory()
        user = UserFactory(is_active=True, is_superuser=True)
        data = get_data_from_factory(cmr, mvs, delete=True, superuser=user)
        request = APIRequestFactory().post("", data=data)
        request.user = user
        kwargs = {}
        view = mvs.as_view({"post": "create"})
        response = view(request, kwargs).render()
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("instance")
        assert response.data["instance"]["client"] == cmr.client.id


@pytest.mark.django_db
class TestUserIsClientViewSet:
    @pytest.mark.parametrize("mvs", [UserIsClientViewSet])
    def test_get(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        obj = PersonFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=user, relationship_manager=obj)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 1
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsClientViewSet])
    def test_retrieve(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        user = Person.get_or_create_with_user(request.user)
        rel = ClientManagerRelationshipFactory(client=user)
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=rel.pk)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsClientViewSet])
    def test_delete(self, mvs):
        request = APIRequestFactory().delete("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        obj = PersonFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=user, relationship_manager=obj)
        view = mvs.as_view({"delete": "destroy"})
        with pytest.raises(AttributeError):
            view(request, pk=obj.id).render()


@pytest.mark.django_db
class TestUserIsManagerViewSet:
    @pytest.mark.parametrize("mvs", [UserIsManagerViewSet])
    def test_get(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        obj = EntryFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=obj, relationship_manager=user)
        vs = mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 1
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsManagerViewSet])
    def test_retrieve(self, mvs):
        request = APIRequestFactory().get("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        obj = EntryFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=obj, relationship_manager=user)
        vs = mvs.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.pk)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("mvs", [UserIsManagerViewSet])
    def test_delete(self, mvs):
        request = APIRequestFactory().delete("")
        request.user = UserFactory(is_active=True, is_superuser=True)
        obj = EntryFactory()
        user = Person.get_or_create_with_user(request.user)
        ClientManagerRelationshipFactory(client=obj, relationship_manager=user)
        view = mvs.as_view({"delete": "destroy"})
        response = view(request, pk=obj.id).render()
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestContactViewsets:
    @pytest.mark.parametrize(
        "mvs",
        [
            EmailContactEntryViewSet,
            AddressContactEntryViewSet,
            TelephoneContactEntryViewSet,
            WebsiteContactEntryViewSet,
            BankingContactEntryViewSet,
            SocialMediaContactEntryViewSet,
        ],
    )
    def test_get_propagated_contact(self, mvs, internal_user_factory):
        request = APIRequestFactory().get("")
        request.user = get_or_create_superuser()
        factory = get_model_factory(mvs.queryset.model)
        obj = factory(entry=internal_user_factory().profile)
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"get": "list"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        assert response.data.get("results")

    @pytest.mark.parametrize(
        "mvs",
        [
            EmailContactEntryViewSet,
            AddressContactEntryViewSet,
            TelephoneContactEntryViewSet,
            WebsiteContactEntryViewSet,
            BankingContactEntryViewSet,
            SocialMediaContactEntryViewSet,
        ],
    )
    def test_post_delete_contact(self, mvs):
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        user = get_or_create_superuser()
        data = get_data_from_factory(obj, mvs, delete=True, superuser=user)
        request = APIRequestFactory().post("", data)
        request.user = user
        kwargs = get_kwargs(obj, mvs, request=request, data=data)
        vs = mvs.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("instance")

    @pytest.mark.parametrize(
        "mvs",
        [
            EmailContactEntryViewSet,
            AddressContactEntryViewSet,
            TelephoneContactEntryViewSet,
            WebsiteContactEntryViewSet,
            BankingContactEntryViewSet,
            SocialMediaContactEntryViewSet,
        ],
    )
    def test_primary_DeleteEndpointMixin(self, mvs):
        request = APIRequestFactory().delete("")
        request.user = get_or_create_superuser()
        factory = get_model_factory(mvs.queryset.model)
        obj = factory()
        obj.primary = False
        obj.save()
        kwargs = get_kwargs(obj, mvs, request)
        vs = mvs.as_view({"delete": "destroy_multiple"})
        response = vs(request=request, **kwargs, pk=obj.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT
