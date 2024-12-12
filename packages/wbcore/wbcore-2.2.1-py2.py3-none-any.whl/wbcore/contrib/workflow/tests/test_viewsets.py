from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory
from wbcore.contrib.authentication.factories import GroupFactory, UserFactory
from wbcore.contrib.authentication.models import Permission
from wbcore.contrib.directory.factories import EmailContactFactory, PersonFactory
from wbcore.contrib.directory.models import Person
from wbcore.contrib.workflow.models import EmailStep, ProcessStep, Step
from wbcore.contrib.workflow.sites import workflow_site
from wbcore.contrib.workflow.viewsets import (
    AssignedProcessStepModelViewSet,
    EmailStepModelViewSet,
    ProcessStepModelViewSet,
    WorkflowModelViewSet,
)
from wbcore.test.utils import get_data_from_factory, get_kwargs, get_or_create_superuser


@pytest.mark.django_db
class TestWorkflow:
    api_factory = APIRequestFactory()

    def test_get(self, workflow_factory):
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        workflow_factory.create_batch(3)
        vs = WorkflowModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 3
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, workflow_factory):
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        obj = workflow_factory()
        vs = WorkflowModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.id)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    def test_post(self, workflow_factory):
        obj = workflow_factory()
        super_user = get_or_create_superuser()
        data = get_data_from_factory(obj, WorkflowModelViewSet, superuser=super_user, delete=True)
        request = self.api_factory.post("", data=data)
        request.user = super_user
        kwargs = get_kwargs(obj, WorkflowModelViewSet, request)
        vs = WorkflowModelViewSet.as_view({"post": "create"})
        workflow_site.registered_model_classes_serializer_map[
            Person
        ] = "wbcore.contrib.directory.serializers.PersonModelSerializer"
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete(self, workflow_factory):
        request = self.api_factory.delete("")
        request.user = get_or_create_superuser()
        obj = workflow_factory()
        kwargs = get_kwargs(obj, WorkflowModelViewSet, request)
        vs = WorkflowModelViewSet.as_view({"delete": "destroy"})
        response = vs(request, **kwargs, pk=obj.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_put(self, workflow_factory):
        old_obj = workflow_factory()
        new_obj = workflow_factory()
        user = get_or_create_superuser()
        data = get_data_from_factory(new_obj, WorkflowModelViewSet, superuser=user, delete=True)
        request = self.api_factory.put("", data=data)
        request.user = user
        vs = WorkflowModelViewSet.as_view({"put": "update"})
        workflow_site.registered_model_classes_serializer_map[
            Person
        ] = "wbcore.contrib.directory.serializers.PersonModelSerializer"
        response = vs(request, pk=old_obj.id)
        assert response.status_code == status.HTTP_200_OK

    def test_patch(self, workflow_factory):
        obj = workflow_factory()
        request = self.api_factory.patch("", data={"name": "New Name"})
        request.user = get_or_create_superuser()
        vs = WorkflowModelViewSet.as_view({"patch": "partial_update"})
        workflow_site.registered_model_classes_serializer_map[
            Person
        ] = "wbcore.contrib.directory.serializers.PersonModelSerializer"
        response = vs(request, pk=obj.id)
        assert response.status_code == status.HTTP_200_OK

    @patch("wbcore.contrib.workflow.models.workflow.Workflow.start_workflow")
    def test_start_without_attached_instance(self, mock_start, workflow_factory, start_step_factory):
        workflow = workflow_factory(model=None, status_field=None, preserve_instance=False)
        start_step = start_step_factory(workflow=workflow)
        request = self.api_factory.patch("")
        request.GET = request.GET.copy()
        request.GET["step_id"] = start_step.pk
        user = get_or_create_superuser()
        request.user = user
        response = WorkflowModelViewSet().start(request, pk=workflow.pk)
        assert response.status_code == status.HTTP_200_OK
        assert mock_start.call_args.args == (start_step, None)

    @patch("wbcore.contrib.workflow.models.workflow.Workflow.start_workflow")
    def test_start_with_attached_instance(self, mock_start, workflow_factory, start_step_factory):
        attached_person = PersonFactory()
        workflow = workflow_factory(preserve_instance=True)
        start_step = start_step_factory()
        request = self.api_factory.patch("")
        request.GET = request.GET.copy()
        request.GET["step_id"] = start_step.pk
        request.GET["instance_id"] = attached_person.pk
        user = get_or_create_superuser()
        request.user = user
        response = WorkflowModelViewSet().start(request, pk=workflow.pk)
        assert response.status_code == status.HTTP_200_OK
        assert mock_start.call_args.args == (
            start_step,
            attached_person,
        )


@pytest.mark.django_db
class TestEmailStep:
    api_factory = APIRequestFactory()

    def test_get(self, email_step_factory):
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        email_step_factory.create_batch(3)
        vs = EmailStepModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 3
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, email_step_factory):
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        obj = email_step_factory()
        vs = EmailStepModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.id)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    def test_post(self, email_step_factory):
        super_user = get_or_create_superuser()
        email_contact = EmailContactFactory()
        obj = email_step_factory(to=[email_contact])
        data = {
            "name": obj.name,
            "template": obj.template.open(mode="rb"),
            "step_type": obj.step_type,
            "subject": obj.subject,
            "to": obj.to.all().values_list("id", flat=True),
            "workflow": obj.workflow.id,
            "code": obj.code,
            "status": obj.status,
        }
        request = self.api_factory.post("", data=data)
        request.user = super_user
        EmailStep.objects.filter(pk=obj.pk).delete()
        kwargs = get_kwargs(obj, EmailStepModelViewSet, request)
        vs = EmailStepModelViewSet.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        kwargs.pop("workflow_id")
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete(self, email_step_factory):
        request = self.api_factory.delete("")
        request.user = get_or_create_superuser()
        obj = email_step_factory()
        kwargs = get_kwargs(obj, EmailStepModelViewSet, request)
        vs = EmailStepModelViewSet.as_view({"delete": "destroy"})
        response = vs(request, **kwargs, pk=obj.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_put(self, email_step_factory):
        email_contact1 = EmailContactFactory()
        email_contact2 = EmailContactFactory()
        old_obj = email_step_factory(to=[email_contact1])
        new_obj = email_step_factory(to=[email_contact2])
        user = get_or_create_superuser()
        data = {
            "name": new_obj.name,
            "template": new_obj.template.open(mode="rb"),
            "step_type": new_obj.step_type,
            "subject": new_obj.subject,
            "to": new_obj.to.all().values_list("id", flat=True),
            "workflow": new_obj.workflow.id,
            "code": new_obj.code,
            "status": new_obj.status,
        }
        request = self.api_factory.put("", data=data)
        request.user = user
        EmailStep.objects.filter(pk=new_obj.pk).delete()
        vs = EmailStepModelViewSet.as_view({"put": "update"})
        response = vs(request, pk=old_obj.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["name"] == new_obj.name
        assert not response.data["instance"]["name"] == old_obj.name

    def test_patch(self, email_step_factory):
        obj = email_step_factory()
        request = self.api_factory.patch("", data={"name": "New Name"})
        request.user = get_or_create_superuser()
        vs = EmailStepModelViewSet.as_view({"patch": "partial_update"})
        response = vs(request, pk=obj.id)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestProcessStep:
    api_factory = APIRequestFactory()

    def test_get(self, process_step_factory):
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        process_step_factory.create_batch(3)
        vs = ProcessStepModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        assert len(response.data.get("results")) == 3
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, process_step_factory):
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        obj = process_step_factory()
        vs = ProcessStepModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=obj.id)
        assert response.data.get("instance")
        assert not response.data.get("results")
        assert response.status_code == status.HTTP_200_OK

    def test_post(self, process_step_factory):
        obj = process_step_factory()
        super_user = get_or_create_superuser()
        data = get_data_from_factory(obj, ProcessStepModelViewSet, superuser=super_user, delete=True)
        request = self.api_factory.post("", data=data)
        request.user = super_user
        kwargs = get_kwargs(obj, ProcessStepModelViewSet, request)
        vs = ProcessStepModelViewSet.as_view({"post": "create"})
        response = vs(request, **kwargs)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self, process_step_factory):
        request = self.api_factory.delete("")
        request.user = get_or_create_superuser()
        obj = process_step_factory()
        kwargs = get_kwargs(obj, ProcessStepModelViewSet, request)
        vs = ProcessStepModelViewSet.as_view({"delete": "destroy"})
        response = vs(request, **kwargs, pk=obj.pk)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_patch(self, process_step_factory):
        obj = process_step_factory()
        request = self.api_factory.patch("", data={"name": "New Name"})
        request.user = get_or_create_superuser()
        vs = ProcessStepModelViewSet.as_view({"patch": "partial_update"})
        response = vs(request, pk=obj.id)
        assert response.status_code == status.HTTP_200_OK

    def test_get_queryset_superuser(self, process_step_factory):
        process_step1 = process_step_factory(permission=Permission.objects.first())
        process_step2 = process_step_factory()
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        mvs = ProcessStepModelViewSet(request=request, kwargs={})
        assert set(str(x.pk) for x in mvs.get_queryset()) == {process_step2.pk, process_step1.pk}

    def test_get_queryset_user_permission(self, process_step_factory):
        permission = Permission.objects.first()
        process_step1 = process_step_factory(permission=permission)
        process_step2 = process_step_factory()
        request = self.api_factory.get("")
        user = UserFactory()
        user.user_permissions.add(permission)
        request.user = user
        mvs = ProcessStepModelViewSet(request=request, kwargs={})
        assert set(str(x.pk) for x in mvs.get_queryset()) == {process_step2.pk, process_step1.pk}

    def test_get_queryset_group_permission(self, process_step_factory):
        permission = Permission.objects.first()
        process_step1 = process_step_factory(permission=permission)
        process_step2 = process_step_factory()
        request = self.api_factory.get("")
        group = GroupFactory(permissions=[permission])
        request.user = UserFactory(groups=[group])
        mvs = ProcessStepModelViewSet(request=request, kwargs={})
        assert set(str(x.pk) for x in mvs.get_queryset()) == {process_step1.pk, process_step2.pk}

    def test_get_queryset_no_permission(self, process_step_factory):
        process_step_factory(permission=Permission.objects.first())
        process_step2 = process_step_factory()
        request = self.api_factory.get("")
        request.user = UserFactory()
        mvs = ProcessStepModelViewSet(request=request, kwargs={})
        assert set(str(x.pk) for x in mvs.get_queryset()) == {process_step2.pk}

    @patch("wbcore.contrib.workflow.models.step.Step.start_next_step")
    def test_next(self, mock_next, process_step_factory, transition_factory):
        process_step = process_step_factory()
        transition = transition_factory()
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        request.GET = request.GET.copy()
        request.GET["transition_id"] = transition.pk
        response = ProcessStepModelViewSet().next(request, pk=process_step.pk)
        assert response.status_code == status.HTTP_200_OK
        assert set(str(x.pk) for x in mock_next.call_args.args) == {process_step.pk, str(transition.pk)}

    @pytest.mark.parametrize(
        "bad_types",
        [
            Step.StepType.DECISIONSTEP,
            Step.StepType.EMAILSTEP,
            Step.StepType.FINISHSTEP,
            Step.StepType.JOINSTEP,
            Step.StepType.SCRIPTSTEP,
            Step.StepType.SPLITSTEP,
        ],
    )
    @pytest.mark.parametrize(
        "bad_states",
        [
            ProcessStep.StepState.CANCELED,
            ProcessStep.StepState.FAILED,
            ProcessStep.StepState.FINISHED,
            ProcessStep.StepState.WAITING,
        ],
    )
    def test_assigned_process_steps(self, process_step_factory, user_step_factory, bad_types, bad_states):
        request = self.api_factory.get("")
        group = GroupFactory()
        user = UserFactory(groups=[group], is_superuser=True)
        request.user = user
        step = user_step_factory(assignee_method=None)
        process_step1 = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE, assignee=user)
        process_step2 = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE, group=group)
        process_step_factory(step__step_type=bad_types, state=ProcessStep.StepState.ACTIVE, assignee=user)
        process_step_factory(step=step, state=bad_states, assignee=user)
        vs = AssignedProcessStepModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.data.get("results")
        assert not response.data.get("instance")
        id_set = {x["id"] for x in response.data.get("results")}
        assert id_set == {str(process_step1.pk), str(process_step2.pk)}
        assert response.status_code == status.HTTP_200_OK
