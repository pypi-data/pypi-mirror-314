from django.utils.translation import gettext as _
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import IntegerPreference, StringPreference

wbcore = Section("wbcore")


@global_preferences_registry.register
class RetentionPeriod(IntegerPreference):
    section = wbcore
    name = "retention_period"
    default = 365

    verbose_name = _("Retention Period in Days")
    help_text = _(
        "When an object cannot be deleted and is disabled instead, it gets hidden from the queryset but not deleted. For compliance reasons we enable the retention for a specific period of days (defaults to a year)"
    )


@global_preferences_registry.register
class SystemUserEmailPeriod(StringPreference):
    section = wbcore
    name = "system_user_email"

    default = "system@stainly-bench.com"

    verbose_name = _("System User Email")
    help_text = _("System User Email")
