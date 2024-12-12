import pytest
from django_fsm import TransitionNotAllowed
from dynamic_preferences.registries import global_preferences_registry
from wbcore.contrib.directory.models import ClientManagerRelationship as CMR
from wbcore.contrib.directory.models import Company, Person
from wbcore.contrib.directory.models.entries import handle_user_deactivation

from ..factories import ClientManagerRelationshipFactory as CMRF


@pytest.mark.django_db
class TestSpecificModelsContacts:
    def test_set_entry_primary_telephone(self, telephone_contact_factory):
        tc = telephone_contact_factory()
        tc2 = telephone_contact_factory()

        tc.set_entry_primary_telephone(tc.entry, tc2.number)
        assert str(tc.entry.primary_telephone_contact()) == str(tc2.entry.primary_telephone_contact())

        tc3 = telephone_contact_factory(primary=False)
        tc3.primary = False
        tc3.save()
        tc3.set_entry_primary_telephone(tc3.entry, tc2.number)
        assert str(tc3.entry.primary_telephone_contact()) == str(tc2.entry.primary_telephone_contact())

    def test_set_entry_primary_email(self, email_contact_factory):
        ec = email_contact_factory()
        ec2 = email_contact_factory()

        ec.set_entry_primary_email(ec.entry, ec2.address)
        assert ec.entry.primary_email_contact().id != ec2.entry.primary_email_contact().id
        assert ec.entry.primary_email_contact().address == ec2.entry.primary_email_contact().address

        ec3 = email_contact_factory(primary=False)
        ec3.primary = False
        ec3.save()
        ec3.set_entry_primary_email(ec3.entry, ec2.address)
        assert ec3.entry.primary_email_contact().id != ec2.entry.primary_email_contact().id
        assert ec3.entry.primary_email_contact().address == ec2.entry.primary_email_contact().address


@pytest.mark.django_db
class TestSpecificModelsEntries:
    def test_primary_email_contact(self, person_factory, company_factory):
        assert company_factory().primary_email_contact() is None
        assert person_factory().primary_email_contact() is None

    def test_primary_telephone_contact(self, person_factory, company_factory):
        assert company_factory().primary_telephone_contact() is None
        assert person_factory().primary_telephone_contact() is None

    def test_primary_address_contact(self, person_factory, company_factory):
        assert company_factory().primary_address_contact() is None
        assert person_factory().primary_address_contact() is None

    def test_primary_website_contact(self, person_factory, company_factory):
        assert company_factory().primary_website_contact() is None
        assert person_factory().primary_website_contact() is None

    def test_primary_banking_contact(self, person_factory, company_factory):
        assert company_factory().primary_banking_contact() is None
        assert person_factory().primary_banking_contact() is None

    def test_get_casted_entry(self, person_factory, company_factory):
        assert company_factory().get_casted_entry()
        assert person_factory().get_casted_entry()

    def test_delete_additional_fields(self, person_factory, company_factory):
        person1 = person_factory()
        person1.additional_fields["special_key"] = "additionnal fields special key"
        person1.delete_additional_fields("special_key")
        assert "special_key" not in person1.additional_fields.keys()

    def test_full_name(self, person_factory, company_factory, internal_user_factory):
        assert person_factory().full_name
        person = internal_user_factory().profile
        person.employers.add(company_factory())
        assert person.str_full()

    # Tests for CRM user deactivation method
    def test_main_company_removed_from_deactivated_user(self, internal_user_factory):
        old_person = internal_user_factory().profile
        main_company_id = global_preferences_registry.manager()["directory__main_company"]
        main_company = Company.objects.get(id=main_company_id)
        assert (
            handle_user_deactivation(sender=None, instance=old_person, substitute_profile=None)[0]
            == f"Removed {main_company.computed_str} from {old_person.computed_str}'s employers"
        )
        assert main_company not in old_person.employers.all()

    def test_no_substitute_person(self, client_manager_relationship_factory, internal_user_factory):
        person = internal_user_factory().profile
        relationship = client_manager_relationship_factory(relationship_manager=person)
        handle_user_deactivation(sender=None, instance=person, substitute_profile=None)
        assert CMR.objects.get(id=relationship.id).status == CMR.Status.REMOVED

    def test_not_approved_substitute_relationships_exists(
        self, client_manager_relationship_factory, person_factory, internal_user_factory
    ):
        old_person = internal_user_factory().profile
        new_person = person_factory()
        old_relationship = client_manager_relationship_factory(
            relationship_manager=old_person, status=CMR.Status.PENDINGADD
        )
        substitute_relationship = client_manager_relationship_factory(
            client=old_relationship.client, relationship_manager=new_person
        )
        assert (
            handle_user_deactivation(sender=None, instance=old_person, substitute_profile=new_person)[1]
            == f"Assigned 1 manager role(s) to {new_person.computed_str}"
        )
        assert not CMR.objects.filter(id=old_relationship.id).exists()
        assert CMR.objects.get(id=substitute_relationship.id).client.id == old_relationship.client.id
        assert CMR.objects.get(id=substitute_relationship.id).relationship_manager.id == new_person.id

    def test_not_approved_substitute_relationships_missing(
        self, client_manager_relationship_factory, person_factory, internal_user_factory
    ):
        old_person = internal_user_factory().profile
        new_person = person_factory()
        old_relationship = client_manager_relationship_factory(
            relationship_manager=old_person, status=CMR.Status.PENDINGADD
        )
        assert (
            handle_user_deactivation(sender=None, instance=old_person, substitute_profile=new_person)[1]
            == f"Assigned 1 manager role(s) to {new_person.computed_str}"
        )
        assert CMR.objects.get(id=old_relationship.id).relationship_manager.id == new_person.id
        assert CMR.objects.get(id=old_relationship.id).client.id == old_relationship.client.id

    def test_approved_with_substitute_relationships(
        self, client_manager_relationship_factory, person_factory, internal_user_factory
    ):
        old_person = internal_user_factory().profile
        new_person = person_factory()
        old_relationship = client_manager_relationship_factory(relationship_manager=old_person, primary=True)
        client_manager_relationship_factory(relationship_manager=old_person)
        substitute_relationship = client_manager_relationship_factory(
            client=old_relationship.client, relationship_manager=new_person, status=CMR.Status.PENDINGADD
        )
        assert (
            handle_user_deactivation(sender=None, instance=old_person, substitute_profile=new_person)[1]
            == f"Assigned 2 manager role(s) to {new_person.computed_str}"
        )
        assert CMR.objects.get(id=substitute_relationship.id).client.id == old_relationship.client.id
        assert CMR.objects.get(id=substitute_relationship.id).relationship_manager.id == new_person.id
        assert CMR.objects.get(id=substitute_relationship.id).status == CMR.Status.APPROVED
        assert CMR.objects.get(id=substitute_relationship.id).primary is True

    def test_approved_without_substitute_relationships_needs_primary(
        self, client_manager_relationship_factory, person_factory, internal_user_factory
    ):
        old_person = internal_user_factory().profile
        new_person = person_factory()
        old_relationship = client_manager_relationship_factory(relationship_manager=old_person, primary=True)
        assert (
            handle_user_deactivation(sender=None, instance=old_person, substitute_profile=new_person)[1]
            == f"Assigned 1 manager role(s) to {new_person.computed_str}"
        )
        assert CMR.objects.filter(
            relationship_manager=new_person, client=old_relationship.client, primary=True, status=CMR.Status.APPROVED
        ).exists()
        assert CMR.objects.get(id=old_relationship.id).status == CMR.Status.REMOVED

    def test_approved_without_substitute_relationships_doesnt_need_primary(
        self, client_manager_relationship_factory, person_factory, internal_user_factory
    ):
        old_person = internal_user_factory().profile
        new_person = person_factory()
        old_relationship = client_manager_relationship_factory(relationship_manager=old_person)
        client_manager_relationship_factory(client=old_relationship.client, primary=True)
        assert (
            handle_user_deactivation(sender=None, instance=old_person, substitute_profile=new_person)[1]
            == f"Assigned 1 manager role(s) to {new_person.computed_str}"
        )
        assert CMR.objects.filter(
            relationship_manager=new_person, client=old_relationship.client, primary=False, status=CMR.Status.APPROVED
        ).exists()
        assert CMR.objects.get(id=old_relationship.id).status == CMR.Status.REMOVED

    def test_soft_deleted_entry_dont_show_in_queryset(self, company_factory, person_factory):
        "ensure the default queryset filter out soft deleted entries"
        person = person_factory.create()
        assert set(Person.objects.all()) == {person}

        person.delete()
        assert not Person.objects.exists()

        company = company_factory.create()
        assert set(Company.objects.all()) == {company}

        company.delete()
        assert not Company.objects.exists()

    def test_soft_deleted_person_doesnt_crash_user_registration(self, user_factory, email_contact_factory):
        user = user_factory(profile=None)
        email_contact_factory(address=user.email, entry__is_active=False)
        assert Person.get_or_create_with_user(user)


@pytest.mark.django_db
class TestSpecificModelsClientManagerRelationship:
    @pytest.mark.parametrize("status, expected", [("DRAFT", "PENDINGADD")])
    def test_submit(self, status, expected):
        cmr = CMRF(status=CMR.Status.DRAFT)
        cmr.submit()
        assert cmr.status == expected

    @pytest.mark.parametrize("status, expected", [("PENDINGADD", "APPROVED")])
    def test_approve(self, status, expected):
        cmr = CMRF(status=CMR.Status.PENDINGADD)
        cmr.approve()
        assert cmr.status == expected

    @pytest.mark.parametrize("status, expected", [("PENDINGADD", "DRAFT")])
    def test_deny(self, status, expected):
        cmr = CMRF(status=CMR.Status.PENDINGADD)
        cmr.deny()
        assert cmr.status == expected

    @pytest.mark.parametrize("status, expected", [("DRAFT", "APPROVED")])
    def test_mngapprove(self, status, expected):
        cmr = CMRF(status=CMR.Status.DRAFT)
        cmr.mngapprove()
        assert cmr.status == expected

    @pytest.mark.parametrize("status, expected", [("PENDINGREMOVE", "APPROVED")])
    def test_denyremoval(self, status, expected):
        cmr = CMRF(status=CMR.Status.PENDINGREMOVE)
        cmr.denyremoval()
        assert cmr.status == expected

    @pytest.mark.parametrize("status, expected", [("PENDINGREMOVE", "REMOVED")])
    def test_approveremoval(self, status, expected):
        cmr = CMRF(status=CMR.Status.PENDINGREMOVE)
        cmr.approveremoval()
        assert cmr.status == expected

    @pytest.mark.parametrize("status, expected", [("APPROVED", "PENDINGADD")])
    def test_makeprimary(self, status, expected):
        cmr1 = CMRF(primary=True)
        cmr2 = CMRF(primary=False, client=cmr1.client)
        cmr2.makeprimary()
        assert cmr2.status == expected
        assert cmr2.primary
        with pytest.raises(TransitionNotAllowed):
            cmr1.makeprimary()
        assert cmr1.status == status
        assert cmr1.primary

    @pytest.mark.parametrize("status, expected", [("APPROVED", "PENDINGREMOVE")])
    def test_remove(self, status, person, expected):
        cmr1 = CMRF.create(primary=True, client=person)
        cmr2 = CMRF.create(primary=False, client=person)
        cmr2.remove()
        assert cmr2.status == expected
        with pytest.raises(TransitionNotAllowed):
            cmr1.remove()
        assert cmr1.status == status

    @pytest.mark.parametrize("status, expected", [("REMOVED", "PENDINGADD")])
    def test_reinstate(self, status, expected):
        cmr = CMRF(status=CMR.Status.REMOVED)
        cmr.reinstate()
        assert cmr.status == expected


@pytest.mark.django_db
class TestSpecificModelsRelationships:
    def test_relationship_type_str(self, relationship_type_factory):
        assert relationship_type_factory(title="Type").__str__() == "Type"

    def test_relationship_str(self, relationship_factory, relationship_type_factory, person_factory):
        relationship_type = relationship_type_factory(
            title="Type",
            counter_relationship=None,
        )
        from_entry = person_factory(first_name="John", last_name="Doe")
        to_entry = person_factory(first_name="Jane", last_name="Doe")
        rel = relationship_factory(
            relationship_type=relationship_type,
            from_entry=from_entry,
            to_entry=to_entry,
        )
        assert rel.__str__() == "John Doe is Type of Jane Doe"
