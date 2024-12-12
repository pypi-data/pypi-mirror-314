from unittest.mock import patch

import pytest
from wbcore.contrib.directory.factories import PersonFactory
from wbcore.contrib.workflow.models import Condition


@pytest.mark.django_db
class TestDecisionStep:
    def test_get_first_valid_transition(
        self, process_step_factory, decision_step_factory, transition_factory, condition_factory
    ):
        attached_instance = PersonFactory()
        step = decision_step_factory()
        process_step = process_step_factory(process__instance=attached_instance, step=step)
        valid_transition1 = transition_factory(from_step=step)
        valid_transition2 = transition_factory(from_step=step)
        invalid_transition = transition_factory(from_step=step)
        transition_factory()
        condition_factory(
            transition=invalid_transition,
            attribute_name="first_name",
            expected_value=attached_instance.first_name,
            operator=Condition.Operator.EQ,
            negate_operator=True,
        )
        assert step.get_first_valid_transition(process_step) in [valid_transition1, valid_transition2]

    def test_get_first_valid_transition_no_transitions(
        self, process_step_factory, decision_step_factory, transition_factory, condition_factory
    ):
        attached_instance = PersonFactory()
        step = decision_step_factory()
        process_step = process_step_factory(process__instance=attached_instance, step=step)
        invalid_transition = transition_factory(from_step=step)
        transition_factory()
        condition_factory(
            transition=invalid_transition,
            attribute_name="first_name",
            expected_value=attached_instance.first_name,
            operator=Condition.Operator.EQ,
            negate_operator=True,
        )
        assert step.get_first_valid_transition(process_step) is None

    @patch("wbcore.contrib.workflow.models.step.DecisionStep.get_first_valid_transition")
    @patch("wbcore.contrib.workflow.models.step.Step.start_next_step")
    def test_run(
        self,
        mock_next,
        mock_transition,
        process_step_factory,
        transition_factory,
        decision_step_factory,
    ):
        transition = transition_factory()
        mock_transition.return_value = transition
        step = decision_step_factory()
        process_step = process_step_factory(step=step)
        step.run(process_step)
        assert mock_next.call_args.args == (process_step, transition)

    @patch("wbcore.contrib.workflow.models.step.Step.set_failed")
    @patch("wbcore.contrib.workflow.models.step.activate_step.delay")
    @patch("wbcore.contrib.workflow.models.step.DecisionStep.get_first_valid_transition")
    def test_run_failed(
        self,
        mock_transition,
        mock_activate,
        mock_failed,
        process_step_factory,
        decision_step_factory,
    ):
        mock_transition.return_value = None
        step = decision_step_factory()
        process_step = process_step_factory(step=step)
        step.run(process_step)
        assert mock_failed.call_args.args[0] == process_step
        assert not mock_activate.called
