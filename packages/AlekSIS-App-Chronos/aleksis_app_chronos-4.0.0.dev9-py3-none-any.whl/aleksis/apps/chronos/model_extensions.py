from django.utils.translation import gettext_lazy as _

from aleksis.apps.cursus.models import Course
from aleksis.core.models import Group, Person, Room

# Dynamically add permissions to Group, Person and Room models in core and Course model in cursus
# Note: requires migrate afterwards
Group.add_permission(
    "view_group_timetable",
    _("Can view group timetable"),
)
Group.add_permission(
    "manage_group_substitutions",
    _("Can manage group substitutions"),
)
Person.add_permission(
    "view_person_timetable",
    _("Can view person timetable"),
)
Group.add_permission(
    "view_group_supervisions",
    _("Can view group supervisions"),
)
Person.add_permission(
    "view_person_supervisions",
    _("Can view person supervisions"),
)
Room.add_permission(
    "view_room_supervisions",
    _("Can view room supervisions"),
)
Course.add_permission(
    "view_course_timetable",
    _("Can view course timetable"),
)
