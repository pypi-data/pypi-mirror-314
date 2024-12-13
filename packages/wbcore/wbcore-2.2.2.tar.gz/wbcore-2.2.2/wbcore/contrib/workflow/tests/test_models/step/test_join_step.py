from unittest.mock import patch

import pytest
from wbcore.contrib.workflow.models import ProcessStep


@pytest.mark.django_db
class TestJoinStep:
    @patch("wbcore.contrib.workflow.models.step.Step.set_canceled")
    def test_cancel_if_leading_to_self_transition_found(
        self, mock_canceled, random_child_step_factory, join_step_factory, process_step_factory, transition_factory
    ):
        self_step = join_step_factory()
        step = random_child_step_factory()
        process_step = process_step_factory(step=step)
        transition1 = transition_factory(from_step=step)
        transition_factory(from_step=step)
        transition_factory(from_step=transition1.to_step, to_step=self_step)
        transition_factory()
        self_step.cancel_if_leading_to_self(step, process_step)
        assert mock_canceled.call_args.args == (process_step,)

    @patch("wbcore.contrib.workflow.models.step.Step.set_canceled")
    def test_cancel_if_leading_to_self_no_transition_found(
        self,
        mock_canceled,
        random_child_step_factory,
        join_step_factory,
        process_step_factory,
        transition_factory,
    ):
        self_step = join_step_factory()
        step = random_child_step_factory()
        process_step = process_step_factory(step=step)
        transition1 = transition_factory(from_step=step)
        transition_factory(from_step=step)
        transition_factory(from_step=transition1.to_step)
        transition_factory()
        self_step.cancel_if_leading_to_self(step, process_step)
        assert not mock_canceled.called

    @patch("wbcore.contrib.workflow.models.step.JoinStep.cancel_if_leading_to_self")
    @patch("wbcore.contrib.workflow.models.step.Step.execute_single_next_step")
    def test_run_wait_for_all_transition_without_process_step(
        self, mock_execute, mock_cancel, process_step_factory, join_step_factory, transition_factory
    ):
        step = join_step_factory(wait_for_all=True)
        transition_factory(to_step=step)
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        step.run(process_step)
        assert process_step.state == ProcessStep.StepState.WAITING
        assert not mock_execute.called
        assert not mock_cancel.called

    @patch("wbcore.contrib.workflow.models.step.JoinStep.cancel_if_leading_to_self")
    @patch("wbcore.contrib.workflow.models.step.Step.execute_single_next_step")
    def test_run_wait_for_all_transition_with_process_step(
        self, mock_execute, mock_cancel, process_step_factory, join_step_factory, transition_factory
    ):
        step = join_step_factory(wait_for_all=True)
        transition = transition_factory(to_step=step)
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        process_step_factory(
            step=transition.from_step, process=process_step.process, state=ProcessStep.StepState.ACTIVE
        )
        step.run(process_step)
        assert process_step.state == ProcessStep.StepState.WAITING
        assert not mock_execute.called
        assert not mock_cancel.called

    @pytest.mark.parametrize("state", [ProcessStep.StepState.FINISHED, ProcessStep.StepState.CANCELED])
    @patch("wbcore.contrib.workflow.models.step.JoinStep.cancel_if_leading_to_self")
    @patch("wbcore.contrib.workflow.models.step.Step.execute_single_next_step")
    def test_run_wait_for_all_transition_with_finished_canceled_process_step(
        self, mock_execute, mock_cancel, process_step_factory, join_step_factory, transition_factory, state
    ):
        step = join_step_factory(wait_for_all=True)
        transition = transition_factory(to_step=step)
        transition_factory(from_step=step)
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        process_step_factory(step=transition.from_step, process=process_step.process, state=state)
        step.run(process_step)
        assert process_step.state == ProcessStep.StepState.WAITING
        assert mock_execute.call_args.args == (process_step,)
        assert not mock_cancel.called

    @patch("wbcore.contrib.workflow.models.step.JoinStep.cancel_if_leading_to_self")
    @patch("wbcore.contrib.workflow.models.step.Step.execute_single_next_step")
    def test_run_wait_for_all_no_transition(
        self, mock_execute, mock_cancel, process_step_factory, join_step_factory, transition_factory
    ):
        step = join_step_factory(wait_for_all=True)
        transition_factory(from_step=step)
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        step.run(process_step)
        assert process_step.state == ProcessStep.StepState.WAITING
        assert mock_execute.call_args.args == (process_step,)
        assert not mock_cancel.called

    @patch("wbcore.contrib.workflow.models.step.JoinStep.cancel_if_leading_to_self")
    @patch("wbcore.contrib.workflow.models.step.Step.execute_single_next_step")
    def test_run_do_not_wait(
        self,
        mock_execute,
        mock_cancel,
        process_step_factory,
        join_step_factory,
    ):
        step = join_step_factory(wait_for_all=False)
        process_step = process_step_factory(step=step, state=ProcessStep.StepState.ACTIVE)
        unfinished_process_step1 = process_step_factory(
            process=process_step.process, state=ProcessStep.StepState.ACTIVE
        )
        unfinished_process_step2 = process_step_factory(
            process=process_step.process, state=ProcessStep.StepState.WAITING
        )
        process_step_factory(state=ProcessStep.StepState.ACTIVE)
        process_step_factory(process=process_step.process, state=ProcessStep.StepState.FINISHED)
        process_step_factory(process=process_step.process, state=ProcessStep.StepState.CANCELED)
        process_step_factory(process=process_step.process, state=ProcessStep.StepState.FAILED)
        step.run(process_step)
        assert process_step.state == ProcessStep.StepState.WAITING
        assert mock_execute.call_args.args == (process_step,)
        assert set(tuple(map(lambda y: str(y.pk), x.args)) for x in mock_cancel.call_args_list) == {
            (str(unfinished_process_step1.step.pk), unfinished_process_step1.pk),
            (str(unfinished_process_step2.step.pk), unfinished_process_step2.pk),
        }
