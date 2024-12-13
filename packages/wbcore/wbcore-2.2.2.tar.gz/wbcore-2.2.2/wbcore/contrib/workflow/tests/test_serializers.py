import pytest
from rest_framework.test import APIRequestFactory
from wbcore.contrib.authentication.factories import GroupFactory, UserFactory
from wbcore.contrib.workflow.models import ProcessStep, Step
from wbcore.contrib.workflow.serializers import (
    AssignedProcessStepSerializer,
    ProcessStepModelSerializer,
)
from wbcore.test.utils import get_or_create_superuser


@pytest.mark.django_db
class TestProcessStep:
    api_factory = APIRequestFactory()

    def test_next_process_step_buttons_superuser(self, transition_factory, process_step_factory, user_step_factory):
        step = user_step_factory()
        transition1 = transition_factory(
            from_step=step,
        )
        transition2 = transition_factory(
            from_step=step,
        )
        transition_factory(to_step=step)
        transition_factory()
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        transition_labels = {x["label"] for x in serializer.data["_buttons"]}
        assert transition_labels == {transition1.name, transition2.name}

    def test_next_process_step_buttons_assignee(self, transition_factory, process_step_factory, user_step_factory):
        step = user_step_factory()
        transition = transition_factory(
            from_step=step,
        )
        user = UserFactory()
        process_step = process_step_factory(assignee=user, step=step, state=ProcessStep.StepState.ACTIVE)
        request = self.api_factory.get("")
        request.user = user
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        assert serializer.data["_buttons"][0]["label"] == transition.name

    def test_next_process_step_buttons_group(self, transition_factory, process_step_factory, user_step_factory):
        step = user_step_factory(assignee_method=None)
        transition = transition_factory(
            from_step=step,
        )
        group = GroupFactory()
        user = UserFactory(groups=[group])
        process_step = process_step_factory(group=group, step=step, state=ProcessStep.StepState.ACTIVE)
        request = self.api_factory.get("")
        request.user = user
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        assert serializer.data["_buttons"][0]["label"] == transition.name

    @pytest.mark.parametrize(
        "state",
        [
            ProcessStep.StepState.CANCELED,
            ProcessStep.StepState.FAILED,
            ProcessStep.StepState.FINISHED,
            ProcessStep.StepState.WAITING,
        ],
    )
    def test_next_process_step_buttons_not_active(
        self, state, transition_factory, process_step_factory, user_step_factory
    ):
        step = user_step_factory()
        transition_factory(
            from_step=step,
        )
        process_step = process_step_factory(step=step, state=state)
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        assert serializer.data["_buttons"] == []

    @pytest.mark.parametrize(
        "step_type",
        [
            Step.StepType.DECISIONSTEP,
            Step.StepType.EMAILSTEP,
            Step.StepType.FINISHSTEP,
            Step.StepType.JOINSTEP,
            Step.StepType.SCRIPTSTEP,
            Step.StepType.SPLITSTEP,
        ],
    )
    def test_next_process_step_buttons_not_user_step(
        self, step_type, transition_factory, process_step_factory, step_factory
    ):
        step = step_factory(step_type=step_type)
        transition_factory(
            from_step=step,
        )
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        assert serializer.data["_buttons"] == []

    def test_next_process_step_buttons_not_assigned(self, transition_factory, process_step_factory, user_step_factory):
        step = user_step_factory()
        transition_factory(
            from_step=step,
        )
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        request = self.api_factory.get("")
        request.user = UserFactory()
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        assert serializer.data["_buttons"] == []

    def test_next_process_step_buttons_assigned_group_with_method(
        self, transition_factory, process_step_factory, user_step_factory
    ):
        step = user_step_factory()
        transition_factory(
            from_step=step,
        )
        group = GroupFactory()
        user = UserFactory(groups=[group])
        process_step = process_step_factory(group=group, step=step, state=ProcessStep.StepState.ACTIVE)
        request = self.api_factory.get("")
        request.user = user
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        assert serializer.data["_buttons"] == []

    def test_next_process_step_buttons_no_transitions(
        self, transition_factory, process_step_factory, user_step_factory
    ):
        step = user_step_factory()
        transition_factory()
        transition_factory(to_step=step)
        transition_factory()
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        serializer = ProcessStepModelSerializer(process_step, context={"request": request})
        assert serializer.data
        assert serializer.data["_buttons"] == []


@pytest.mark.django_db
class TestAssignedProcessStep:
    api_factory = APIRequestFactory()

    def test_get_instance_endpoint_no_request(self, process_step_factory):
        process_step = process_step_factory()
        serializer = AssignedProcessStepSerializer(process_step)
        assert serializer.data
        assert serializer.data["instance_endpoint"] == ""

    def test_get_instance_endpoint_no_attached_instance(self, process_step_factory):
        process_step = process_step_factory(process__instance=None, process__instance_id=None)
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        serializer = AssignedProcessStepSerializer(process_step, context={"request": request})
        assert serializer.data
        assert "processstep" in serializer.data["instance_endpoint"]

    def test_get_instance_endpoint_attached_instance(self, process_step_factory):
        process_step = process_step_factory()
        request = self.api_factory.get("")
        request.user = get_or_create_superuser()
        serializer = AssignedProcessStepSerializer(process_step, context={"request": request})
        assert serializer.data
        assert "processstep" not in serializer.data["instance_endpoint"]
        assert "person" in serializer.data["instance_endpoint"]
