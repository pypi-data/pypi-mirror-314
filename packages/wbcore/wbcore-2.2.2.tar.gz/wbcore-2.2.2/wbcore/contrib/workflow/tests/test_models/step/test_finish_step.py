from unittest.mock import patch

import pytest
from wbcore.contrib.directory.models import Person
from wbcore.contrib.workflow.models import Process, ProcessStep
from wbcore.contrib.workflow.sites import workflow_site


@pytest.mark.django_db
class TestFinishStep:
    @pytest.mark.parametrize(
        "finished_state",
        [ProcessStep.StepState.FAILED, ProcessStep.StepState.CANCELED, ProcessStep.StepState.FINISHED],
    )
    @pytest.mark.parametrize("unfinished_state", [ProcessStep.StepState.ACTIVE, ProcessStep.StepState.WAITING])
    @patch("wbcore.contrib.workflow.models.step.Step.set_finished")
    def test_run(self, mock_finish, process_step_factory, finish_step_factory, unfinished_state, finished_state):
        step = finish_step_factory()
        process_step = process_step_factory(step=step)
        process_step_factory(process=process_step.process, state=finished_state)
        process_step_factory(step=step, state=unfinished_state)
        step.run(process_step)
        assert mock_finish.call_args.args == (process_step,)

    @pytest.mark.parametrize("unfinished_state", [ProcessStep.StepState.ACTIVE, ProcessStep.StepState.WAITING])
    @patch("wbcore.contrib.workflow.models.step.Step.set_failed")
    def test_run_failed(self, mock_failed, process_step_factory, finish_step_factory, unfinished_state):
        step = finish_step_factory()
        process_step = process_step_factory(step=step)
        process_step_factory(process=process_step.process, state=unfinished_state)
        step.run(process_step)
        assert mock_failed.call_args.args[0] == process_step

    @pytest.mark.parametrize(
        "unfinished_state",
        [
            ProcessStep.StepState.ACTIVE,
            ProcessStep.StepState.WAITING,
            ProcessStep.StepState.CANCELED,
            ProcessStep.StepState.FAILED,
        ],
    )
    @patch("wbcore.contrib.workflow.models.step.Step.finish")
    def test_finish_not_finished(self, mock_finish, unfinished_state, process_step_factory, finish_step_factory):
        step = finish_step_factory(write_preserved_instance=True)
        process_step = process_step_factory(
            process__preserved_instance={"first_name": "Test"},
            step=step,
            process__finished=None,
            state=unfinished_state,
            process__state=Process.ProcessState.ACTIVE,
        )
        step.finish(process_step)
        assert mock_finish.call_args.args == (process_step,)
        assert process_step.process.finished is None
        assert process_step.process.instance.first_name != "Test"
        assert process_step.process.state == Process.ProcessState.ACTIVE

    @patch("wbcore.contrib.workflow.models.step.Step.finish")
    def test_finish_write_preserved_instance(self, mock_finish, process_step_factory, finish_step_factory):
        step = finish_step_factory(write_preserved_instance=True, workflow__preserve_instance=True)
        process_step = process_step_factory(
            step=step,
            process__finished=None,
            state=ProcessStep.StepState.FINISHED,
            process__workflow=step.workflow,
        )
        old_name = process_step.process.instance.first_name
        workflow_site.registered_model_classes_serializer_map[
            Person
        ] = "wbcore.contrib.directory.serializers.PersonModelSerializer"
        step.finish(process_step)
        assert mock_finish.call_args.args == (process_step,)
        assert process_step.process.finished is not None
        assert process_step.process.instance.first_name != old_name
        assert process_step.process.instance.first_name == process_step.process.preserved_instance["first_name"]
        assert process_step.process.state == Process.ProcessState.FINISHED

    @patch("wbcore.contrib.workflow.models.step.Step.finish")
    def test_finish_do_not_write(self, mock_finish, process_step_factory, finish_step_factory):
        step = finish_step_factory(write_preserved_instance=False, workflow__preserve_instance=True)
        process_step = process_step_factory(
            step=step,
            process__finished=None,
            state=ProcessStep.StepState.FINISHED,
        )
        old_name = process_step.process.instance.first_name
        step.finish(process_step)
        assert mock_finish.call_args.args == (process_step,)
        assert process_step.process.finished is not None
        assert process_step.process.instance.first_name == old_name
        assert process_step.process.state == Process.ProcessState.FINISHED

    @patch("wbcore.contrib.workflow.models.step.Step.finish")
    def test_finish_no_preserved_instance(self, mock_finish, process_step_factory, finish_step_factory):
        step = finish_step_factory(write_preserved_instance=True, workflow__preserve_instance=True)
        process_step = process_step_factory(
            step=step, process__finished=None, state=ProcessStep.StepState.FINISHED, process__preserved_instance=None
        )
        old_name = process_step.process.instance.first_name
        step.finish(process_step)
        assert mock_finish.call_args.args == (process_step,)
        assert process_step.process.finished is not None
        assert process_step.process.instance.first_name == old_name
        assert process_step.process.state == Process.ProcessState.FINISHED
