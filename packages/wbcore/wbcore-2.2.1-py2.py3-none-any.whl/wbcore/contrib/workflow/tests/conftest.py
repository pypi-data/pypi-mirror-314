import pytest
from django.apps import apps
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.signals import pre_migrate
from pytest_factoryboy import register
from wbcore.contrib.geography.tests.signals import app_pre_migration
from wbcore.contrib.workflow.factories import (
    ConditionFactory,
    DataFactory,
    DataValueFactory,
    DecisionStepFactory,
    EmailStepFactory,
    FinishStepFactory,
    JoinStepFactory,
    ProcessFactory,
    ProcessStepFactory,
    RandomChildStepFactory,
    ScriptStepFactory,
    SplitStepFactory,
    StartStepFactory,
    StepFactory,
    TransitionFactory,
    UserStepFactory,
    WorkflowFactory,
)
from wbcore.tests.conftest import *

register(WorkflowFactory)
register(EmailStepFactory)
register(TransitionFactory)
register(DataFactory)
register(ProcessStepFactory)
register(UserStepFactory)
register(ConditionFactory)
register(RandomChildStepFactory)
register(FinishStepFactory)
register(ProcessFactory)
register(DecisionStepFactory)
register(SplitStepFactory)
register(JoinStepFactory)
register(ScriptStepFactory)
register(StepFactory)
register(DataValueFactory)
register(StartStepFactory)


@pytest.fixture(autouse=True, scope="session")
def django_test_environment(django_test_environment):
    from django.apps import apps

    get_models = apps.get_models

    for m in [m for m in get_models() if not m._meta.managed]:
        m._meta.managed = True


pre_migrate.connect(app_pre_migration, sender=apps.get_app_config("geography"))
