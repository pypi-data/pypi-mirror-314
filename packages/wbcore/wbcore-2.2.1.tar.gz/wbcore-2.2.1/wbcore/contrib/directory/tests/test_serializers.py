from unittest import TestCase

import pytest
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from schwifty import IBAN
from wbcore.contrib.directory.models import ClientManagerRelationship as CMR
from wbcore.contrib.directory.serializers import (
    AddressContactSerializer,
    BankingContactSerializer,
    EmailContactSerializer,
    RelationshipTypeRepresentationSerializer,
    TelephoneContactSerializer,
    WebsiteContactSerializer,
)

from ..factories import (
    AddressContactFactory,
    BankingContactFactory,
    EmailContactFactory,
    EntryFactory,
    PersonFactory,
    TelephoneContactFactory,
    WebsiteContactFactory,
)
from ..viewsets import ClientManagerViewSet, RelationshipModelViewSet


@pytest.mark.django_db
class TestRelationshipTypeSerializers:
    def test_serialize_model(self, relationship_type_factory):
        APIRequestFactory().get("")
        type = relationship_type_factory(title="Test Type")
        serializer = RelationshipTypeRepresentationSerializer(type)

        assert serializer.data
        assert serializer.data["title"] == "Test Type"


@pytest.mark.django_db
class TestRelationshipSerializers:
    def test_serialize_model(self, relationship_factory):
        relationship_factory()
        mvs = RelationshipModelViewSet()
        qs = mvs.get_serializer_class().Meta.model.objects.all()
        qs = mvs.serializer_class()
        assert qs.data


@pytest.mark.django_db
class TestClientManagerSerializers(TestCase):
    def test_create_existing_request(self):
        """
        Validate method should fail when given data for an already existing client manager relationship.
        """
        manager = PersonFactory()
        client = PersonFactory(relationship_managers=[manager])
        relationship = CMR.objects.filter(relationship_manager=manager, client=client)
        relationship.update(primary=True)

        mvs = ClientManagerViewSet()
        serializer = mvs.serializer_class()
        data = {
            "client": client,
            "relationship_manager": manager,
            "primary": True,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_create_new_request(self):
        """
        Validate method should not fail when given data for a new relationship.
        """
        manager = PersonFactory()
        client = PersonFactory()
        mvs = ClientManagerViewSet()
        serializer = mvs.serializer_class()
        data = {
            "client": client,
            "relationship_manager": manager,
        }
        try:
            validated_data = serializer.validate(data)
        except DjangoValidationError:
            self.fail("New client manager relationship threw error in validation method!")
        else:
            self.assertEqual(validated_data, data)

    def test_self_relationship_managers(self):
        """
        Validate method should fail when client and manager are the same person.
        """
        person = PersonFactory()
        mvs = ClientManagerViewSet()
        serializer = mvs.serializer_class()
        data = {
            "client": person,
            "relationship_manager": person,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_degrade_primary_manager(self):
        """
        Validate method should fail when trying to make primary manager non-primary.
        """
        manager = PersonFactory()
        client = PersonFactory(relationship_managers=[manager])

        mvs = ClientManagerViewSet()
        serializer = mvs.serializer_class()
        data = {
            "client": client,
            "relationship_manager": manager,
            "primary": False,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)


@pytest.mark.django_db
class TestContactSerializers(TestCase):
    def test_create_email_duplicates(self):
        """
        Validate method should fail when given data for an already existing email contact.
        """
        entry = EntryFactory()
        email = EmailContactFactory(entry=entry)

        serializer = EmailContactSerializer()
        data = {
            "entry": entry,
            "address": email.address,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_create_banking_duplicates(self):
        """
        Validate method should fail when given data for an already existing banking contact.
        """
        entry = EntryFactory()
        BankingContactFactory(entry=entry, iban=IBAN("AD1400080001001234567890").formatted)

        serializer = BankingContactSerializer()
        data = {
            "entry": entry,
            "iban": IBAN("AD1400080001001234567890").formatted,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_create_telephone_duplicates(self):
        """
        Validate method should fail when given data for an already existing telephone contact.
        """
        entry = EntryFactory()
        phone = TelephoneContactFactory(entry=entry)

        serializer = TelephoneContactSerializer()
        data = {
            "entry": entry,
            "number": phone.number,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_create_website_duplicates(self):
        """
        Validate method should fail when given data for an already existing website contact.
        """
        entry = EntryFactory()
        website = WebsiteContactFactory(entry=entry)

        serializer = WebsiteContactSerializer()
        data = {
            "entry": entry,
            "url": website.url,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)

    def test_create_address_duplicates(self):
        """
        Validate method should fail when given data for an already existing address contact.
        """
        entry = EntryFactory()
        address = AddressContactFactory(entry=entry)

        serializer = AddressContactSerializer()
        data = {
            "entry": entry,
            "street": address.street,
            "street_additional": address.street_additional,
            "zip": address.zip,
            "geography_city": address.geography_city,
        }
        with self.assertRaises(ValidationError):
            serializer.validate(data)
