from unittest.mock import patch

import pytest
from wbcore.contrib.authentication.factories import GroupFactory, UserFactory
from wbcore.contrib.directory.factories import ClientFactory
from wbcore.contrib.workflow.models import ProcessStep, Step
from wbcore.contrib.workflow.workflows import (
    manager_of_instance_assignee,
    random_group_member,
    weighted_random,
)


@pytest.mark.django_db
class TestWorkflowAssignees:
    def test_manager_of_instance_assignee_person(self, process_step_factory):
        kwargs = {"assignee_field": "profile", "assignee_type": "entry"}
        attached_instance = UserFactory()
        process_step = process_step_factory(process__instance=attached_instance)
        manager_list = ClientFactory.create_batch(3, clients=[attached_instance.profile])
        UserFactory(profile=manager_list[1], is_active=False)
        UserFactory(profile=manager_list[2])
        assert manager_of_instance_assignee(process_step, **kwargs) == manager_list[2].user_account

    def test_manager_of_instance_assignee_no_kwargs(self, process_step_factory):
        process_step = process_step_factory()
        assert not manager_of_instance_assignee(process_step)
        assert process_step.state == ProcessStep.StepState.FAILED

    def test_manager_of_instance_assignee_no_assignee_field(self, process_step_factory):
        kwargs = {"test": "profile", "assignee_type": "entry"}
        process_step = process_step_factory()
        assert not manager_of_instance_assignee(process_step, **kwargs)
        assert process_step.state == ProcessStep.StepState.FAILED

    def test_manager_of_instance_assignee_no_assignee_type(self, process_step_factory):
        kwargs = {"assignee_field": "profile", "test": "entry"}
        process_step = process_step_factory()
        assert not manager_of_instance_assignee(process_step, **kwargs)
        assert process_step.state == ProcessStep.StepState.FAILED

    def test_manager_of_instance_assignee_wrong_assignee_field(self, process_step_factory):
        kwargs = {"assignee_field": "profile", "assignee_type": "entry"}
        process_step = process_step_factory()
        assert not manager_of_instance_assignee(process_step, **kwargs)
        assert process_step.state == ProcessStep.StepState.FAILED

    def test_manager_of_instance_assignee_wrong_assignee_type(self, process_step_factory):
        kwargs = {"assignee_field": "profile", "assignee_type": "test"}
        attached_instance = UserFactory()
        process_step = process_step_factory(process__instance=attached_instance)
        assert not manager_of_instance_assignee(process_step, **kwargs)
        assert process_step.state == ProcessStep.StepState.FAILED

    @pytest.mark.parametrize(
        "bad_states", [ProcessStep.StepState.FAILED, ProcessStep.StepState.CANCELED, ProcessStep.StepState.WAITING]
    )
    @pytest.mark.parametrize(
        "bad_types",
        [
            Step.StepType.DECISIONSTEP,
            Step.StepType.EMAILSTEP,
            Step.StepType.FINISHSTEP,
            Step.StepType.JOINSTEP,
            Step.StepType.SPLITSTEP,
            Step.StepType.SCRIPTSTEP,
        ],
    )
    @patch("wbcore.contrib.workflow.workflows.assignees.choices")
    def test_weighted_random(self, mock_choices, user_step_factory, process_step_factory, bad_states, bad_types):
        group = GroupFactory()
        process_step = process_step_factory(group=group)
        assignee1 = UserFactory(groups=[group])
        assignee2 = UserFactory(groups=[group])
        user_step = user_step_factory()
        process_step_factory(
            state=ProcessStep.StepState.ACTIVE,
            process=process_step.process,
            group=process_step.group,
            step=user_step,
            assignee=assignee1,
        )
        process_step_factory(
            state=ProcessStep.StepState.FINISHED,
            process=process_step.process,
            group=process_step.group,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.FINISHED,
            process=process_step.process,
            group=process_step.group,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=bad_states,
            process=process_step.process,
            group=process_step.group,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.ACTIVE,
            group=process_step.group,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.ACTIVE,
            process=process_step.process,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.FINISHED,
            process=process_step.process,
            group=process_step.group,
            step__step_type=bad_types,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.FINISHED,
            process=process_step.process,
            group=process_step.group,
            step=user_step,
        )
        assert weighted_random(process_step)
        assert len(mock_choices.call_args.args) == 1
        assert len(mock_choices.call_args.kwargs) == 1
        assignees_with_weights = set(zip(mock_choices.call_args.args[0], mock_choices.call_args.kwargs["weights"]))
        assert assignees_with_weights == {(assignee1, 2 / 3), (assignee2, 1 / 3)}

    @pytest.mark.parametrize(
        "bad_states", [ProcessStep.StepState.FAILED, ProcessStep.StepState.CANCELED, ProcessStep.StepState.WAITING]
    )
    @pytest.mark.parametrize(
        "bad_types",
        [
            Step.StepType.DECISIONSTEP,
            Step.StepType.EMAILSTEP,
            Step.StepType.FINISHSTEP,
            Step.StepType.JOINSTEP,
            Step.StepType.SPLITSTEP,
            Step.StepType.SCRIPTSTEP,
        ],
    )
    @patch("wbcore.contrib.workflow.workflows.assignees.choices")
    def test_weighted_random_no_past_ocurrences(
        self, mock_choices, user_step_factory, process_step_factory, bad_states, bad_types
    ):
        group = GroupFactory()
        process_step = process_step_factory(group=group)
        assignee1 = UserFactory(groups=[group])
        assignee2 = UserFactory(groups=[group])
        user_step = user_step_factory()

        process_step_factory(
            state=bad_states,
            process=process_step.process,
            group=process_step.group,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.ACTIVE,
            group=process_step.group,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.ACTIVE,
            process=process_step.process,
            step=user_step,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.FINISHED,
            process=process_step.process,
            group=process_step.group,
            step__step_type=bad_types,
            assignee=assignee2,
        )
        process_step_factory(
            state=ProcessStep.StepState.FINISHED,
            process=process_step.process,
            group=process_step.group,
            step=user_step,
        )
        assert weighted_random(process_step)
        assert len(mock_choices.call_args.args) == 1
        assert set(mock_choices.call_args.args[0]) == {assignee1, assignee2}
        assert not mock_choices.call_args.kwargs

    @patch("wbcore.contrib.workflow.workflows.assignees.choices")
    def test_weighted_random_no_group(self, mock_choices, process_step_factory):
        process_step = process_step_factory()
        assert not weighted_random(process_step)
        assert not mock_choices.called
        assert process_step.state == ProcessStep.StepState.FAILED

    @patch("wbcore.contrib.workflow.workflows.assignees.choices")
    def test_weighted_random_no_group_members(self, mock_choices, process_step_factory):
        process_step = process_step_factory(group=GroupFactory())
        assert not weighted_random(process_step)
        assert not mock_choices.called
        assert process_step.state == ProcessStep.StepState.FAILED

    def test_random_group_member(self, process_step_factory):
        group = GroupFactory()
        process_step = process_step_factory(group=group)
        UserFactory(groups=[group])
        UserFactory(groups=[group])
        assert random_group_member(process_step)

    def test_random_group_member_no_group(self, process_step_factory):
        process_step = process_step_factory()
        assert not random_group_member(process_step)
        assert process_step.state == ProcessStep.StepState.FAILED

    def test_random_group_member_no_group_members(self, process_step_factory):
        process_step = process_step_factory(group=GroupFactory())
        assert not random_group_member(process_step)
        assert process_step.state == ProcessStep.StepState.FAILED
