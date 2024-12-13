import factory
from django.db.models import signals
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.workflow.models import Transition


@factory.django.mute_signals(signals.post_save)
class TransitionFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("text", max_nb_chars=128)
    to_step = factory.SubFactory("wbcore.contrib.workflow.factories.RandomChildStepFactory")
    from_step = factory.SubFactory("wbcore.contrib.workflow.factories.RandomChildStepFactory")
    icon = factory.Iterator(WBIcon.values)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Both steps need to belong to the same workflow
        if (from_step := kwargs.get("from_step")) and (to_step := kwargs.get("to_step")):
            if kwargs["from_step"].workflow != kwargs["to_step"].workflow:
                from_step.workflow = to_step.workflow
                from_step.save()
                kwargs["from_step"] = from_step
        return super()._create(model_class, *args, **kwargs)

    class Meta:
        model = Transition
