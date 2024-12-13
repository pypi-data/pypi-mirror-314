from unittest.mock import patch

import pytest
from django.template import TemplateSyntaxError
from wbcore.contrib.directory.factories import EmailContactFactory


@pytest.mark.django_db
class TestEmailStep:
    @patch("wbcore.contrib.workflow.models.step.Step.execute_single_next_step")
    @patch("django.core.mail.EmailMultiAlternatives.__init__")
    @patch("django.core.mail.EmailMultiAlternatives.send")
    @patch("django.core.mail.EmailMultiAlternatives.attach_alternative")
    def test_run(self, mock_attach, mock_send, mock_init, mock_execute, process_step_factory, email_step_factory):
        step = email_step_factory(to=[EmailContactFactory()], cc=[EmailContactFactory(), EmailContactFactory()])
        process_step = process_step_factory(step=step)
        mock_init.return_value = None
        step.run(process_step)
        assert mock_init.call_args.args[0] == step.subject
        assert mock_init.call_args.kwargs == {
            "to": list(step.to.values_list("address", flat=True)),
            "cc": list(step.cc.values_list("address", flat=True)),
            "bcc": [],
        }
        assert mock_attach.called
        assert mock_send.called
        assert mock_execute.call_args.args == (process_step,)

    @patch("wbcore.contrib.workflow.models.step.Step.set_failed")
    @patch("django.template.Template.render")
    @patch("wbcore.contrib.workflow.models.step.Step.execute_single_next_step")
    @patch("django.core.mail.EmailMultiAlternatives.send")
    def test_run_failed(
        self, mock_send, mock_execute, mock_render, mock_set_failed, process_step_factory, email_step_factory
    ):
        step = email_step_factory(
            to=[EmailContactFactory()],
            cc=[EmailContactFactory(), EmailContactFactory()],
        )
        process_step = process_step_factory(step=step)
        mock_render.side_effect = TemplateSyntaxError
        step.run(process_step)
        assert not mock_send.called
        assert not mock_execute.called
        assert mock_set_failed.call_args.args[0] == process_step
