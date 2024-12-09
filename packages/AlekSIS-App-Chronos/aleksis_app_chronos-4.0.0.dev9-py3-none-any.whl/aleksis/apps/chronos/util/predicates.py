from django.contrib.auth.models import User
from django.db.models import Model

from rules import predicate

from aleksis.apps.cursus.models import Course
from aleksis.core.models import Group, Person, Room
from aleksis.core.util.core_helpers import queryset_rules_filter
from aleksis.core.util.predicates import has_any_object, has_global_perm, has_object_perm

from ..models import LessonEvent
from .chronos_helpers import get_groups, get_rooms, get_teachers


@predicate
def has_timetable_perm(user: User, obj: Model) -> bool:
    """
    Check if can access timetable.

    Predicate which checks whether the user is allowed
    to access the requested timetable.
    """
    if isinstance(obj, Group):
        return has_group_timetable_perm(user, obj)
    elif isinstance(obj, Person):
        return has_person_timetable_perm(user, obj)
    elif isinstance(obj, Room):
        return has_room_timetable_perm(user, obj)
    elif isinstance(obj, Course):
        return has_course_timetable_perm(user, obj)
    else:
        return False


@predicate
def has_group_timetable_perm(user: User, obj: Group) -> bool:
    """
    Check if can access group timetable.

    Predicate which checks whether the user is allowed
    to access the requested group timetable.
    """
    return (
        obj in user.person.member_of.all()
        or user.person.primary_group == obj
        or obj in user.person.owner_of.all()
        or has_global_perm("chronos.view_all_group_timetables")(user)
        or has_object_perm("core.view_group_timetable")(user, obj)
    )


@predicate
def has_substitution_perm_by_group(user: User, obj: LessonEvent) -> bool:
    """
    Check if can create/edit substitution based on group.

    Predicate which checks whether the user is allowed
    to create/edit the requested substitution.
    """
    return (
        obj.groups.filter(pk__in=user.person.owner_of.values_list("id", flat=True)).exists()
        or queryset_rules_filter(user, obj.groups.all(), "core.manage_group_substitutions").exists()
    )


@predicate
def has_group_substitution_perm(user: User, obj: Group) -> bool:
    """
    Check if can access/edit substitutions of given group.

    Predicate which checks whether the user is allowed
    to access/edit the substitutions of the given group.
    """
    return (
        obj in user.person.owner_of.all()
        or has_global_perm("chronos.view_lessonsubstitution")(user)
        or has_object_perm("core.manage_group_substitutions")(user, obj)
    )


@predicate
def has_any_group_substitution_perm(user: User) -> bool:
    """
    Check if can create/edit substitutions of any group.

    Predicate which checks whether the user is allowed
    to create/edit any substitutions of any group.
    """
    return user.person.owner_of.exists() or has_any_object(
        "core.manage_group_substitutions", Group
    )(user)


@predicate
def has_person_timetable_perm(user: User, obj: Person) -> bool:
    """
    Check if can access person timetable.

    Predicate which checks whether the user is allowed
    to access the requested person timetable.
    """
    return (
        user.person == obj
        or has_global_perm("chronos.view_all_person_timetables")(user)
        or has_object_perm("core.view_person_timetable")(user, obj)
    )


@predicate
def has_room_timetable_perm(user: User, obj: Room) -> bool:
    """
    Check if can access room timetable.

    Predicate which checks whether the user is allowed
    to access the requested room timetable.
    """
    return has_global_perm("chronos.view_all_room_timetables")(user) or has_object_perm(
        "core.view_room_timetable"
    )(user, obj)


@predicate
def has_course_timetable_perm(user: User, obj: Course) -> bool:
    """
    Check if can access course timetable.

    Predicate which checks whether the user is allowed
    to access the requested course timetable.
    """
    return (
        user.person in obj.teachers.all()
        or obj.groups.all().intersection(user.person.member_of.all()).exists()
        or user.person.primary_group in obj.groups.all()
        or obj.groups.all().intersection(user.person.owner_of.all()).exists()
        or has_global_perm("chronos.view_all_course_timetables")(user)
        or has_object_perm("cursus.view_course_timetable")(user, obj)
    )


@predicate
def has_supervisions_perm(user: User, obj: Model) -> bool:
    """
    Check if can access supervisions of object.

    Predicate which checks whether the user is allowed
    to access the requested supervisions of the given
    group, person or room.
    """
    if isinstance(obj, Group):
        return has_group_supervisions_perm(user, obj)
    elif isinstance(obj, Person):
        return has_person_supervisions_perm(user, obj)
    elif isinstance(obj, Room):
        return has_room_supervisions_perm(user, obj)
    else:
        return False


@predicate
def has_group_supervisions_perm(user: User, obj: Group) -> bool:
    """
    Check if can access group supervisions.

    Predicate which checks whether the user is allowed
    to access the requested group supervisions.
    """
    return (
        obj in user.person.member_of.all()
        or user.person.primary_group == obj
        or obj in user.person.owner_of.all()
        or has_global_perm("chronos.view_all_group_supervisions")(user)
        or has_object_perm("core.view_group_supervisions")(user, obj)
    )


@predicate
def has_person_supervisions_perm(user: User, obj: Person) -> bool:
    """
    Check if can access person supervisions.

    Predicate which checks whether the user is allowed
    to access the requested person supervisions.
    """
    return (
        user.person == obj
        or has_global_perm("chronos.view_all_person_supervisions")(user)
        or has_object_perm("core.view_person_supervisions")(user, obj)
    )


@predicate
def has_room_supervisions_perm(user: User, obj: Room) -> bool:
    """
    Check if can access room supervisions.

    Predicate which checks whether the user is allowed
    to access the requested room supervisions.
    """
    return has_global_perm("chronos.view_all_room_supervisions")(user) or has_object_perm(
        "core.view_room_supervisions"
    )(user, obj)


@predicate
def has_any_timetable_object(user: User) -> bool:
    """Predicate which checks whether there are any timetables the user is allowed to access."""
    return get_groups(user).exists() or get_rooms(user).exists() or get_teachers(user).exists()
