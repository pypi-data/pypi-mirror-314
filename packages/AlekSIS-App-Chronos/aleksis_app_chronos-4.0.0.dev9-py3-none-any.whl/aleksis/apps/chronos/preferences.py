from datetime import time

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from calendarweek.django import i18n_day_name_choices_lazy
from colorfield.widgets import ColorWidget
from dynamic_preferences.preferences import Section
from dynamic_preferences.types import (
    BooleanPreference,
    IntegerPreference,
    ModelMultipleChoicePreference,
    MultipleChoicePreference,
    StringPreference,
    TimePreference,
)

from aleksis.core.models import GroupType
from aleksis.core.registries import site_preferences_registry

chronos = Section("chronos", verbose_name=_("Timetables"))


@site_preferences_registry.register
class UseParentGroups(BooleanPreference):
    section = chronos
    name = "use_parent_groups"
    default = False
    verbose_name = _("Use parent groups in timetable views")
    help_text = _(
        "If a lesson or substitution has only one group"
        " and this group has parent groups,"
        " show the parent groups instead of the original group."
    )


@site_preferences_registry.register
class SubstitutionsRelevantDays(MultipleChoicePreference):
    """Relevant days which have substitution plans."""

    section = chronos
    name = "substitutions_relevant_days"
    default = [0, 1, 2, 3, 4]
    verbose_name = _("Relevant days for substitution plans")
    required = True
    choices = i18n_day_name_choices_lazy()

    def validate(self, value):
        for v in value:
            if int(v) not in self.get_choice_values():
                raise ValidationError(f"{v} is not a valid choice")


@site_preferences_registry.register
class SubstitutionsDayChangeTime(TimePreference):
    """Time when substitution plans should switch to the next day."""

    section = chronos
    name = "substitutions_day_change_time"
    default = time(18, 0)
    verbose_name = _("Time when substitution plans switch to the next day")
    required = True


@site_preferences_registry.register
class SubstitutionsPrintNumberOfDays(IntegerPreference):
    section = chronos
    name = "substitutions_print_number_of_days"
    default = 2
    verbose_name = _("Number of days shown on substitutions print view")


@site_preferences_registry.register
class SubstitutionsShowHeaderBox(BooleanPreference):
    section = chronos
    name = "substitutions_show_header_box"
    default = True
    verbose_name = _("Show header box in substitution views")
    help_text = _("The header box shows affected teachers/groups.")


@site_preferences_registry.register
class AffectedGroupsUseParentGroups(BooleanPreference):
    section = chronos
    name = "affected_groups_parent_groups"
    default = True
    verbose_name = _(
        "Show parent groups in header box in substitution views instead of original groups"
    )


@site_preferences_registry.register
class GroupTypesTimetables(ModelMultipleChoicePreference):
    section = chronos
    name = "group_types_timetables"
    required = False
    default = []
    model = GroupType
    verbose_name = _("Group types to show in timetables")
    help_text = _("If you leave it empty, all groups will be shown.")


@site_preferences_registry.register
class LessonEventFeedColor(StringPreference):
    """Color for the lesson calendar feed."""

    section = chronos
    name = "lesson_color"
    default = "#a7ffeb"
    verbose_name = _("Lesson calendar feed color")
    widget = ColorWidget
    required = True


@site_preferences_registry.register
class SupervisionEventFeedColor(StringPreference):
    """Color for the supervision calendar feed."""

    section = chronos
    name = "supervision_color"
    default = "#e6ee9c"
    verbose_name = _("Supervision calendar feed color")
    widget = ColorWidget
    required = True


@site_preferences_registry.register
class DaysInCalendar(MultipleChoicePreference):
    section = chronos
    name = "days_in_calendar"
    default = ["1", "2", "3", "4", "5"]
    verbose_name = _("Days of the week that appear in the timetable")
    choices = [
        ("0", _("Sunday")),
        ("1", _("Monday")),
        ("2", _("Tuesday")),
        ("3", _("Wednesday")),
        ("4", _("Thursday")),
        ("5", _("Friday")),
        ("6", _("Saturday")),
    ]
    required = True
