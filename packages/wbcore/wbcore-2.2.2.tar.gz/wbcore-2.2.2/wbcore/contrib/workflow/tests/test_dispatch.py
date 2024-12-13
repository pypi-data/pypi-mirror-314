from unittest.mock import patch

import pytest
from wbcore.contrib.directory.factories import PersonFactory
from wbcore.contrib.workflow.dispatch import check_workflow_for_instance
from wbcore.contrib.workflow.factories import UserStepFactory
from wbcore.contrib.workflow.models import Process, ProcessStep


@pytest.mark.django_db
class TestDispatch:
    @patch("wbcore.contrib.workflow.models.step.Step.set_failed")
    def test_check_workflow_for_instance_fail_process_steps(
        self, mock_failed, process_step_factory, random_child_step_factory
    ):
        instance = PersonFactory()
        step = random_child_step_factory(exclude_factories=[UserStepFactory])
        process_step1 = process_step_factory(
            step=step,
            state=ProcessStep.StepState.WAITING,
            process__state=Process.ProcessState.ACTIVE,
            process__instance=instance,
        )
        process_step2 = process_step_factory(
            step=step,
            state=ProcessStep.StepState.ACTIVE,
            process__state=Process.ProcessState.ACTIVE,
            process__instance=instance,
        )
        process_step_factory(
            step=step,
            state=ProcessStep.StepState.ACTIVE,
            process__state=Process.ProcessState.ACTIVE,
            process__instance=instance,
            status=instance.first_name,
        )
        process_step_factory(
            step=step,
            state=ProcessStep.StepState.CANCELED,
            process__state=Process.ProcessState.ACTIVE,
            process__instance=instance,
        )
        process_step_factory(
            step=step,
            state=ProcessStep.StepState.FAILED,
            process__state=Process.ProcessState.ACTIVE,
            process__instance=instance,
        )
        process_step_factory(
            step=step,
            state=ProcessStep.StepState.FINISHED,
            process__state=Process.ProcessState.ACTIVE,
            process__instance=instance,
        )
        process_step_factory(
            step=step,
            state=ProcessStep.StepState.ACTIVE,
            process__state=Process.ProcessState.FAILED,
            process__instance=instance,
        )
        process_step_factory(
            step=step,
            state=ProcessStep.StepState.ACTIVE,
            process__state=Process.ProcessState.FINISHED,
            process__instance=instance,
        )
        process_step_factory(
            step=step,
            state=ProcessStep.StepState.ACTIVE,
            process__state=Process.ProcessState.ACTIVE,
            process__instance=PersonFactory(),
        )
        check_workflow_for_instance(instance.__class__, instance, False)
        assert len(mock_failed.call_args_list) == 2
        assert str(mock_failed.call_args_list[0][0][0].pk) == process_step1.pk
        assert str(mock_failed.call_args_list[1][0][0].pk) == process_step2.pk

    @patch("wbcore.contrib.workflow.models.workflow.Workflow.start_workflow")
    @patch("wbcore.contrib.workflow.models.workflow.Workflow.get_start_steps_for_instance")
    def test_check_workflow_for_instance_start_workflow(self, mock_start_steps, mock_start, start_step_factory):
        instance = PersonFactory()
        start_step1 = start_step_factory()
        start_step2 = start_step_factory()
        start_step_factory()
        mock_start_steps.return_value = [start_step1, start_step2]
        check_workflow_for_instance(instance.__class__, instance, False)
        assert mock_start_steps.call_args.args == (instance,)
        assert mock_start.call_args_list == [((start_step1, instance),), ((start_step2, instance),)]
