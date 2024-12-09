from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Optional

from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from guardian.shortcuts import get_objects_for_user

from aleksis.apps.cursus.models import Course
from aleksis.core.models import Announcement, Group, Person, Room
from aleksis.core.util.core_helpers import (
    filter_active_school_term,
    get_active_school_term,
    get_site_preferences,
)

from ..managers import TimetableType
from .build import build_substitutions_list

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model

    User = get_user_model()  # noqa


def get_el_by_pk(
    request: HttpRequest,
    type_: str,
    pk: int,
    prefetch: bool = False,
    *args,
    **kwargs,
):
    if type_ == TimetableType.GROUP.value:
        return get_object_or_404(
            Group.objects.prefetch_related("owners", "parent_groups") if prefetch else Group,
            pk=pk,
        )
    elif type_ == TimetableType.TEACHER.value or type_ == TimetableType.PARTICIPANT.value:
        return get_object_or_404(Person, pk=pk)
    elif type_ == TimetableType.ROOM.value:
        return get_object_or_404(Room, pk=pk)
    elif type_ == TimetableType.COURSE.value:
        return get_object_or_404(Course, pk=pk)
    else:
        return HttpResponseNotFound()


def get_teachers(user: "User", request=None):
    """Get the teachers whose timetables are allowed to be seen by current user."""

    school_term = get_active_school_term(request)

    q = Q(courses_as_teacher__groups__school_term=school_term) | Q(
        courses_as_teacher__groups__school_term=None
    )
    teachers = (
        Person.objects.annotate(course_count=Count("courses_as_teacher", filter=q))
        .filter(course_count__gt=0)
        .order_by("short_name", "last_name")
    )

    if not user.has_perm("chronos.view_all_person_timetables"):
        teachers.filter(
            Q(pk=user.person.pk)
            | Q(pk__in=get_objects_for_user(user, "core.view_person_timetable", teachers))
        )

    teachers = teachers.distinct()

    return teachers


def get_groups(user: "User", request=None):
    """Get the groups whose timetables are allowed to be seen by current user."""

    groups = filter_active_school_term(request, Group.objects.all())

    group_types = get_site_preferences()["chronos__group_types_timetables"]

    if group_types:
        groups = groups.filter(group_type__in=group_types)

    groups = groups.order_by("short_name", "name")

    if not user.has_perm("chronos.view_all_group_timetables"):
        wanted_groups = get_objects_for_user(user, "core.view_group_timetable", groups)

        groups = groups.filter(
            Q(pk__in=wanted_groups)
            | Q(members=user.person)
            | Q(owners=user.person)
            | Q(pk=user.person.primary_group.pk if user.person.primary_group else None)
        )

    groups = groups.distinct()

    return groups


def get_rooms(user: "User"):
    """Get the rooms whose timetables are allowed to be seen by current user."""

    rooms = Room.objects.all().order_by("short_name", "name")

    if not user.has_perm("chronos.view_all_room_timetables"):
        rooms = get_objects_for_user(user, "core.view_room_timetable", rooms)

    rooms = rooms.distinct()

    return rooms


def get_substitutions_context_data(
    wanted_day: date,
    number_of_days: Optional[int] = None,
    show_header_box: Optional[bool] = None,
):
    """Get context data for the substitutions table."""
    context = {}

    day_number = (
        number_of_days or get_site_preferences()["chronos__substitutions_print_number_of_days"]
    )
    show_header_box = (
        show_header_box
        if show_header_box is not None
        else get_site_preferences()["chronos__substitutions_show_header_box"]
    )
    day_contexts = {}

    day = get_next_relevant_day(wanted_day)
    for _i in range(day_number):
        day_contexts[day] = {"day": day}

        subs, affected_teachers, affected_groups = build_substitutions_list(day)
        day_contexts[day]["substitutions"] = subs

        day_contexts[day]["announcements"] = Announcement.objects.on_date(day)

        if show_header_box:
            day_contexts[day]["affected_teachers"] = sorted(
                affected_teachers, key=lambda t: t.short_name or t.full_name
            )
            day_contexts[day]["affected_groups"] = affected_groups

        day = get_next_relevant_day(day + timedelta(days=1))

    context["days"] = day_contexts

    return context


def get_next_relevant_day(current: datetime | date) -> date:
    """Get next relevant day for substitution plans."""
    relevant_days = get_site_preferences()["chronos__substitutions_relevant_days"]
    change_time = get_site_preferences()["chronos__substitutions_day_change_time"]

    if isinstance(current, datetime):
        current_day = current.date()
        if current.time() > change_time:
            current_day += timedelta(days=1)
    else:
        current_day = current

    while str(current_day.weekday()) not in relevant_days:
        current_day += timedelta(days=1)

    return current_day
