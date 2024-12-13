from dynamic_preferences.types import ModelChoicePreference


class CallableDefaultModelChoicePreference(ModelChoicePreference):
    """
    Propose a ModelChoicePreference class where default is allowed to be a callable property. This avoids unnecessary db calls at start

    This type expects a mandatory model attribute and a section of type dynamic_preferences.Section.
    """

    def __init__(self, registry=None):
        self.registry = registry
        self.queryset = self.model.objects.all()
        self.serializer = self.serializer_class(self.model)
        self._setup_signals()

    @property
    def default(self):
        raise NotImplementedError("Default property needs to be defined for this preference type")
