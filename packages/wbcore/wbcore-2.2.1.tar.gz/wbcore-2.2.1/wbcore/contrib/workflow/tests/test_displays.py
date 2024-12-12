import pytest
from rest_framework.test import APIRequestFactory
from wbcore.contrib.color.enums import WBColor
from wbcore.contrib.workflow.models import ProcessStep
from wbcore.contrib.workflow.viewsets.display.process import (
    get_state_formatting,
    get_state_legend,
)


@pytest.mark.django_db
class TestProcessStep:
    api_factory = APIRequestFactory()

    def test_get_state_legend(self):
        color_map = [
            (ProcessStep.StepState.FAILED, WBColor.GREEN_LIGHT.value),
            (ProcessStep.StepState.CANCELED, WBColor.BLUE_LIGHT.value),
        ]
        assert set((y.icon, y.label, y.value) for y in get_state_legend(color_map)[0].items) == {
            (WBColor.GREEN_LIGHT.value, ProcessStep.StepState.FAILED.label, ProcessStep.StepState.FAILED.value),
            (WBColor.BLUE_LIGHT.value, ProcessStep.StepState.CANCELED.label, ProcessStep.StepState.CANCELED.value),
        }

    def test_get_state_formatting(self):
        color_map = [
            (ProcessStep.StepState.WAITING, WBColor.GREY.value),
            (ProcessStep.StepState.ACTIVE, WBColor.YELLOW_DARK.value),
        ]
        assert set(
            (y.style["backgroundColor"], y.condition[1]) for y in get_state_formatting(color_map)[0].formatting_rules
        ) == {
            (WBColor.GREY.value, ProcessStep.StepState.WAITING.value),
            (WBColor.YELLOW_DARK.value, ProcessStep.StepState.ACTIVE.value),
        }

    # @patch("wbcore.contrib.workflow.viewsets.display.process.split_list_into_grid_template_area_sublists")
    # def test_process_step_display_instance_injection(
    #     self, mock_split, data_factory, user_step_factory, process_step_factory
    # ):
    #     request = self.api_factory.get("")
    #     request.user = get_or_create_superuser()
    #     request.query_params = {}
    #     step = user_step_factory()
    #     process_step = process_step_factory(step=step)
    #     data_factory(workflow=process_step.step.workflow)
    #     mvs = ProcessStepModelViewSet(request=request, kwargs={"pk": process_step.pk})
    #     display = mvs.display_config_class(mvs, request).get_instance_display()
    #     assert display.pages[0].layouts["default"].grid_template_areas == step.display.grid_template_areas
    #     assert not mock_split.called

    # @patch("wbcore.contrib.workflow.viewsets.display.process.split_list_into_grid_template_area_sublists")
    # def test_process_step_display_no_userstep(self, mock_split, random_child_step_factory, process_step_factory):
    #     request = self.api_factory.get("")
    #     request.user = get_or_create_superuser()
    #     request.query_params = {}
    #     step = random_child_step_factory(exclude_factories=[UserStepFactory])
    #     process_step = process_step_factory(step=step)
    #     mvs = ProcessStepModelViewSet(request=request, kwargs={"pk": process_step.pk})
    #     display = mvs.display_config_class(mvs, request).get_instance_display()
    #     display_fields = set(itertools.chain.from_iterable(display.pages[0].layouts["default"].grid_template_areas))
    #     person_fields = set(PersonModelSerializer.Meta.fields)
    #     assert not mock_split.called
    #     assert display_fields.intersection(person_fields) == {"id"}

    # @patch("wbcore.contrib.workflow.viewsets.display.process.split_list_into_grid_template_area_sublists")
    # def test_process_step_display_no_display(self, mock_split, user_step_factory, process_step_factory):
    #     request = self.api_factory.get("")
    #     request.user = get_or_create_superuser()
    #     request.query_params = {}
    #     step = user_step_factory(display=None)
    #     process_step = process_step_factory(step=step)
    #     mvs = ProcessStepModelViewSet(request=request, kwargs={"pk": process_step.pk})
    #     display = mvs.display_config_class(mvs, request).get_instance_display()
    #     display_fields = set(itertools.chain.from_iterable(display.pages[0].layouts["default"].grid_template_areas))
    #     person_fields = set(PersonModelSerializer.Meta.fields)
    #     assert not mock_split.called
    #     assert display_fields.intersection(person_fields) == {"id"}

    # @patch("wbcore.contrib.workflow.viewsets.display.process.split_list_into_grid_template_area_sublists")
    # def test_process_step_display_data_injection(
    #     self, mock_split, data_factory, user_step_factory, process_step_factory
    # ):
    #     request = self.api_factory.get("")
    #     request.user = get_or_create_superuser()
    #     request.query_params = {}
    #     step = user_step_factory(display=None)
    #     process_step = process_step_factory(step=step)
    #     data1 = data_factory(workflow=process_step.process.workflow)
    #     data2 = data_factory(workflow=process_step.process.workflow)
    #     data_factory()
    #     data_sublist = ["a", "b", "c"]
    #     mock_split.return_value = data_sublist
    #     mvs = ProcessStepModelViewSet(request=request, kwargs={"pk": process_step.pk})
    #     display = mvs.display_config_class(mvs, request).get_instance_display()
    #     display_fields = set(itertools.chain.from_iterable(display.pages[0].layouts["default"].grid_template_areas))
    #     person_fields = set(PersonModelSerializer.Meta.fields)
    #     assert display_fields.intersection(person_fields) == {"id"}
    #     assert mock_split.call_args.args[0] == [f"data__{str(data1.pk)}", f"data__{str(data2.pk)}"]
    #     for key in data_sublist:
    #         assert key in display_fields

    # @patch("wbcore.contrib.workflow.viewsets.display.process.split_list_into_grid_template_area_sublists")
    # def test_process_step_display_no_display_no_data(
    #     self, mock_split, data_factory, user_step_factory, process_step_factory
    # ):
    #     request = self.api_factory.get("")
    #     request.user = get_or_create_superuser()
    #     request.query_params = {}
    #     step = user_step_factory(display=None)
    #     process_step = process_step_factory(step=step)
    #     data_factory()
    #     data_factory()
    #     mvs = ProcessStepModelViewSet(request=request, kwargs={"pk": process_step.pk})
    #     display = mvs.display_config_class(mvs, request).get_instance_display()
    #     display_fields = set(itertools.chain.from_iterable(display.pages[0].layouts["default"].grid_template_areas))
    #     person_fields = set(PersonModelSerializer.Meta.fields)
    #     assert display_fields.intersection(person_fields) == {"id"}
    #     assert not mock_split.called
