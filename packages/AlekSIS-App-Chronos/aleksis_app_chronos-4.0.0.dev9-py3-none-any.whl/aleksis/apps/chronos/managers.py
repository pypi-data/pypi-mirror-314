from enum import Enum
from typing import Optional, Union

from django.db.models import Q

from aleksis.apps.cursus.models import Course
from aleksis.core.managers import (
    RecurrencePolymorphicQuerySet,
)
from aleksis.core.models import Group, Person, Room


class TimetableType(Enum):
    """Enum for different types of timetables."""

    GROUP = "group"
    TEACHER = "teacher"
    PARTICIPANT = "participant"
    ROOM = "room"
    COURSE = "course"

    @classmethod
    def from_string(cls, s: Optional[str]):
        return cls.__members__.get(s.upper())


class LessonEventQuerySet(RecurrencePolymorphicQuerySet):
    """Queryset with special query methods for lesson events."""

    @staticmethod
    def for_teacher_q(teacher: Union[int, Person]) -> Q:
        """Get all lesson events for a certain person as teacher (including amends)."""
        from .models import LessonEvent

        amended = (
            LessonEvent.objects.filter(amended_by__isnull=False, teachers=teacher)
            .values_list("amended_by__pk", flat=True)
            .union(LessonEvent.objects.filter(teachers=teacher).values_list("pk", flat=True))
        )
        return Q(pk__in=amended)

    def for_teacher(self, teacher: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain person as teacher (including amends)."""
        return self.filter(self.for_teacher_q(teacher)).distinct()

    @staticmethod
    def for_participant_q(person: Union[int, Person]) -> Q:
        """Get all lesson events the person participates in (including amends)."""
        from .models import LessonEvent

        amended = (
            LessonEvent.objects.filter(amended_by__isnull=False, groups__members=person)
            .values_list("amended_by__pk", flat=True)
            .union(LessonEvent.objects.filter(groups__members=person).values_list("pk", flat=True))
        )
        return Q(pk__in=amended)

    def for_teachers(self, teachers: list[Union[int, Person]]) -> "LessonEventQuerySet":
        """Get all lesson events for a list of persons as teacher (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & (Q(teachers__in=teachers))).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(teachers__in=teachers) | Q(pk__in=amended)).distinct()

    def for_participant(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events the person participates in (including amends)."""
        return self.filter(self.for_participant_q(person)).distinct()

    @staticmethod
    def for_group_q(group: Union[int, Group]) -> Q:
        """Get all lesson events for a certain group (including amends/as parent group)."""
        from .models import LessonEvent

        amended = (
            LessonEvent.objects.filter(amended_by__isnull=False, groups=group)
            .values_list("amended_by__pk", flat=True)
            .union(
                LessonEvent.objects.filter(
                    amended_by__isnull=False, groups__parent_groups=group
                ).values_list("amended_by__pk", flat=True)
            )
            .union(LessonEvent.objects.filter(groups=group).values_list("pk", flat=True))
            .union(
                LessonEvent.objects.filter(groups__parent_groups=group).values_list("pk", flat=True)
            )
        )
        return Q(pk__in=amended)

    def for_owner(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events the person owns any group of (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & Q(groups__owners=person)).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(groups__owners=person) | Q(pk__in=amended)).distinct()

    def for_group(self, group: Union[int, Group]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain group (including amends/as parent group)."""
        return self.filter(self.for_group_q(group)).distinct()

    @staticmethod
    def for_room_q(room: Union[int, Room]) -> Q:
        """Get all lesson events for a certain room (including amends)."""
        from .models import LessonEvent

        amended = (
            LessonEvent.objects.filter(amended_by__isnull=False, rooms=room)
            .values_list("amended_by__pk", flat=True)
            .union(LessonEvent.objects.filter(rooms=room).values_list("pk", flat=True))
        )
        return Q(pk__in=amended)

    def for_room(self, room: Union[int, Room]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain room (including amends)."""
        return self.filter(self.for_room_q(room)).distinct()

    @staticmethod
    def for_course_q(course: Union[int, Course]) -> Q:
        """Get all lesson events for a certain course (including amends)."""
        from .models import LessonEvent

        amended = (
            LessonEvent.objects.filter(amended_by__isnull=False, course=course)
            .values_list("amended_by__pk", flat=True)
            .union(LessonEvent.objects.filter(course=course).values_list("pk", flat=True))
        )
        return Q(pk__in=amended)

    def for_course(self, course: Union[int, Course]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain course (including amends)."""
        return self.filter(self.for_course_q(course)).distinct()

    @staticmethod
    def for_person_q(person: Union[int, Person]) -> Q:
        """Get all lesson events for a certain person (as teacher/participant, including amends)."""
        from .models import LessonEvent

        amended = (
            LessonEvent.objects.filter(amended_by__isnull=False, teachers=person)
            .values_list("amended_by__pk", flat=True)
            .union(
                LessonEvent.objects.filter(
                    amended_by__isnull=False, groups__members=person
                ).values_list("amended_by__pk", flat=True)
            )
            .union(LessonEvent.objects.filter(teachers=person).values_list("pk", flat=True))
            .union(LessonEvent.objects.filter(groups__members=person).values_list("pk", flat=True))
        )
        return Q(pk__in=amended)

    def for_person(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain person (as teacher/participant, including amends)."""
        return self.filter(self.for_person_q(person)).distinct()

    @staticmethod
    def related_to_person_q(person: Union[int, Person]) -> Q:
        """Get all lesson events a certain person is allowed to see.

        This includes all lesson events the person is assigned to as
        teacher/participant/group owner/parent group owner,
        including those amended.
        """
        from .models import LessonEvent

        amended = (
            LessonEvent.objects.filter(amended_by__isnull=False, teachers=person)
            .values_list("amended_by__pk", flat=True)
            .union(
                LessonEvent.objects.filter(
                    amended_by__isnull=False, groups__members=person
                ).values_list("amended_by__pk", flat=True)
            )
            .union(
                LessonEvent.objects.filter(
                    amended_by__isnull=False, groups__owners=person
                ).values_list("amended_by__pk", flat=True)
            )
            .union(
                LessonEvent.objects.filter(
                    amended_by__isnull=False, groups__parent_groups__owners=person
                ).values_list("amended_by__pk", flat=True)
            )
            .union(LessonEvent.objects.filter(teachers=person).values_list("pk", flat=True))
            .union(LessonEvent.objects.filter(groups__members=person).values_list("pk", flat=True))
            .union(LessonEvent.objects.filter(groups__owners=person).values_list("pk", flat=True))
            .union(
                LessonEvent.objects.filter(groups__parent_groups__owners=person).values_list(
                    "pk", flat=True
                )
            )
        )
        return Q(pk__in=amended)

    def related_to_person(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events a certain person is allowed to see.

        This includes all lesson events the person is assigned to as
        teacher/participant/group owner/parent group owner,
        including those amended.
        """
        return self.filter(self.related_to_person_q(person)).distinct()

    @staticmethod
    def not_amended_q() -> Q:
        """Get all lesson events that are not amended."""
        return Q(amended_by__isnull=True)

    def not_amended(self) -> "LessonEventQuerySet":
        """Get all lesson events that are not amended."""
        return self.filter(self.not_amended_q())

    @staticmethod
    def not_amending_q() -> Q:
        """Get all lesson events that are not amending other events."""
        return Q(amends__isnull=True)

    def not_amending(self) -> "LessonEventQuerySet":
        """Get all lesson events that are not amending other events."""
        return self.filter(self.not_amending_q())

    @staticmethod
    def amending_q() -> Q:
        """Get all lesson events that are amending other events."""
        return Q(amends__isnull=False)

    def amending(self) -> "LessonEventQuerySet":
        """Get all lesson events that are amending other events."""
        return self.filter(self.amending_q())

    @staticmethod
    def current_changes_q() -> Q:
        """Get all lesson events that are current changes."""
        return Q(amends__isnull=False) | Q(current_change=True)

    def current_changes(self) -> "LessonEventQuerySet":
        """Get all lesson events that are current changes."""
        return self.filter(self.current_changes_q())


class SupervisionEventQuerySet(LessonEventQuerySet):
    pass
