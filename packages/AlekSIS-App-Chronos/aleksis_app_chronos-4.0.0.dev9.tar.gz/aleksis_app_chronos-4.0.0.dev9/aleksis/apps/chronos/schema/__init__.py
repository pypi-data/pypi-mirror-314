from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.db.models import Q

import graphene
import graphene_django_optimizer
from graphene_django import DjangoObjectType
from reversion import create_revision, set_comment, set_user

from aleksis.apps.cursus.models import Subject
from aleksis.core.models import Group, Person, Room
from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    FilterOrderList,
)
from aleksis.core.schema.group import GroupType
from aleksis.core.schema.person import PersonType
from aleksis.core.schema.room import RoomType
from aleksis.core.util.core_helpers import (
    get_site_preferences,
    has_person,
)

from ..models import LessonEvent
from ..util.build import build_substitutions_list
from ..util.chronos_helpers import get_groups, get_rooms, get_teachers


class TimetablePersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "short_name")
        skip_registry = True


class TimetableGroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = ("id", "name", "short_name")
        skip_registry = True


class TimetableRoomType(DjangoObjectType):
    class Meta:
        model = Room
        fields = ("id", "name", "short_name")
        skip_registry = True


class LessonEventType(DjangoObjectType):
    class Meta:
        model = LessonEvent
        fields = (
            "id",
            "title",
            "slot_number_start",
            "slot_number_end",
            "amends",
            "datetime_start",
            "datetime_end",
            "subject",
            "teachers",
            "groups",
            "rooms",
            "course",
            "cancelled",
            "comment",
        )
        filter_fields = {
            "id": ["exact", "lte", "gte"],
        }

    amends = graphene.Field(lambda: LessonEventType, required=False)
    old_id = graphene.ID(required=False)

    @staticmethod
    def resolve_teachers(root: LessonEvent, info, **kwargs):
        if not str(root.pk).startswith("DUMMY") and hasattr(root, "teachers"):
            return root.teachers
        elif root.amends:
            affected_teachers = root.amends.teachers.filter(
                Q(kolego_absences__datetime_start__lte=root.datetime_end)
                & Q(kolego_absences__datetime_end__gte=root.datetime_start)
            )
            return root.amends.teachers.exclude(pk__in=affected_teachers)
        return []

    @staticmethod
    def resolve_groups(root: LessonEvent, info, **kwargs):
        if not str(root.pk).startswith("DUMMY") and hasattr(root, "groups"):
            return root.groups
        elif root.amends:
            return root.amends.groups
        return []

    @staticmethod
    def resolve_rooms(root: LessonEvent, info, **kwargs):
        if not str(root.pk).startswith("DUMMY") and hasattr(root, "rooms"):
            return root.rooms
        elif root.amends:
            return root.amends.rooms
        return []


class AmendLessonBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = LessonEvent
        permissions = ("chronos.edit_substitution_rule",)
        only_fields = (
            "amends",
            "datetime_start",
            "datetime_end",
            "subject",
            "teachers",
            "groups",
            "rooms",
            "cancelled",
            "comment",
        )

    @classmethod
    def before_save(cls, root, info, input, created_objects):  # noqa: A002
        super().before_save(root, info, input, created_objects)
        for obj in created_objects:
            obj.timezone = obj.amends.timezone
        return created_objects


class AmendLessonBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = LessonEvent
        permissions = ("chronos.edit_substitution_rule",)
        only_fields = ("id", "subject", "teachers", "groups", "rooms", "cancelled", "comment")

    @classmethod
    def before_save(cls, root, info, input, updated_objects):  # noqa: A002
        super().before_save(root, info, input, updated_objects)
        for obj in updated_objects:
            obj.timezone = obj.amends.timezone
        return updated_objects


class AmendLessonBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = LessonEvent
        permissions = ("chronos.delete_substitution_rule",)


class SubstitutionInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    subject = graphene.ID(required=False)
    teachers = graphene.List(graphene.ID, required=False)
    rooms = graphene.List(graphene.ID, required=False)

    comment = graphene.String(required=False)
    cancelled = graphene.Boolean(required=False)


class SubstitutionBatchCreateOrUpdateMutation(graphene.Mutation):
    class Arguments:
        input = graphene.List(SubstitutionInputType)

    substitutions = graphene.List(LessonEventType)

    @classmethod
    def create_or_update(cls, info, substitution):
        _id = substitution.id

        # Sadly, we can't use the update_or_create method since we can't check
        # different permissions depending on the operation with it.
        if _id.startswith("DUMMY"):
            dummy, amended_lesson_event_id, datetime_start_iso, datetime_end_iso = _id.split(";")
            amended_lesson_event = LessonEvent.objects.get(id=amended_lesson_event_id)

            datetime_start = datetime.fromisoformat(datetime_start_iso).astimezone(
                amended_lesson_event.timezone
            )
            datetime_end = datetime.fromisoformat(datetime_end_iso).astimezone(
                amended_lesson_event.timezone
            )

            if info.context.user.has_perm("chronos.create_substitution_rule", amended_lesson_event):
                obj = LessonEvent.objects.create(
                    datetime_start=datetime_start,
                    datetime_end=datetime_end,
                    amends=amended_lesson_event,
                    comment=substitution.comment or "",
                    cancelled=substitution.cancelled or False,
                )
                if substitution.subject is not None:
                    obj.subject = Subject.objects.get(pk=substitution.subject)
                if substitution.teachers is not None:
                    obj.teachers.set(Person.objects.filter(pk__in=substitution.teachers))
                if substitution.rooms is not None:
                    obj.rooms.set(Room.objects.filter(pk__in=substitution.rooms))
                obj.save()
                return obj
            raise PermissionDenied()
        else:
            obj = LessonEvent.objects.get(id=_id)

            if not info.context.user.has_perm("chronos.edit_substitution_rule", obj.amends):
                raise PermissionDenied()

            if substitution.subject is not None:
                obj.subject = Subject.objects.get(pk=substitution.subject)
            if substitution.teachers is not None:
                obj.teachers.set(Person.objects.filter(pk__in=substitution.teachers))
            if substitution.rooms is not None:
                obj.rooms.set(Room.objects.filter(pk__in=substitution.rooms))

            if substitution.cancelled is not None:
                obj.cancelled = substitution.cancelled
            if substitution.comment is not None:
                obj.comment = substitution.comment

            obj.save()
            return obj

    @classmethod
    def mutate(cls, root, info, input):  # noqa
        with create_revision():
            set_user(info.context.user)
            set_comment("Updated in substitution overview")
            objs = [cls.create_or_update(info, substitution) for substitution in input]

        return SubstitutionBatchCreateOrUpdateMutation(substitutions=objs)


class TimetableType(graphene.Enum):
    TEACHER = "teacher"
    GROUP = "group"
    ROOM = "room"


class TimetableObjectType(graphene.ObjectType):
    id = graphene.String()  # noqa
    obj_id = graphene.String()
    name = graphene.String()
    short_name = graphene.String()
    type = graphene.Field(TimetableType)  # noqa

    def resolve_obj_id(root, info, **kwargs):
        return root.id

    def resolve_id(root, info, **kwargs):
        return f"{root.type.value}-{root.id}"


class SubstitutionType(graphene.ObjectType):
    """This type contains the logic also contained in the pdf templates."""

    old_groups = graphene.List(GroupType)
    new_groups = graphene.List(GroupType)
    start_slot = graphene.Int()
    end_slot = graphene.Int()
    start_time = graphene.DateTime()
    end_time = graphene.DateTime()
    old_teachers = graphene.List(PersonType)
    new_teachers = graphene.List(PersonType)
    old_subject = graphene.String()
    new_subject = graphene.String()
    old_rooms = graphene.List(RoomType)
    new_rooms = graphene.List(RoomType)
    cancelled = graphene.Boolean()
    notes = graphene.String()

    # TODO: Extract old/new-pattern into own method and reuse?

    def resolve_old_groups(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.amends and le.amends.groups.all():
            return le.amends.groups.all()
        return le.groups.all()

    def resolve_new_groups(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.groups.all() and le.amends and le.amends.groups.all():
            return le.groups.all()
        else:
            return []

    def resolve_start_slot(root, info):
        return root["REFERENCE_OBJECT"].slot_number_start

    def resolve_end_slot(root, info):
        return root["REFERENCE_OBJECT"].slot_number_end

    def resolve_start_time(root, info):
        return root["DTSTART"].dt

    def resolve_end_time(root, info):
        return root["DTEND"].dt

    def resolve_old_teachers(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.amends and le.amends.teachers.all():
            return le.amends.teachers.all()
        return le.teachers.all()

    def resolve_new_teachers(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.teachers.all() and le.amends and le.amends.teachers.all():
            return le.teachers.all()
        else:
            return []

    def resolve_old_subject(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.name == "supervision":
            return "SUPERVISION"
        elif not (le.amends and le.amends.subject) and not le.subject:
            if le.amends:
                return le.amends.title
            return le.title
        else:
            subject = le.amends.subject if le.amends and le.amends.subject else le.subject
            return subject.short_name or subject.name

    def resolve_new_subject(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.name == "supervision":
            return None
        elif le.subject and le.amends and le.amends.subject:
            return le.subject.short_name or le.subject.name
        else:
            return None

    def resolve_old_rooms(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.amends and le.amends.rooms.all():
            return le.amends.rooms.all()
        return le.rooms.all()

    def resolve_new_rooms(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.rooms.all() and le.amends and le.amends.rooms.all():
            return le.rooms.all()
        else:
            return []

    def resolve_cancelled(root, info):
        return root["REFERENCE_OBJECT"].cancelled

    def resolve_notes(root, info):
        return root["REFERENCE_OBJECT"].comment


class SubstitutionsForDateType(graphene.ObjectType):
    affected_teachers = graphene.List(PersonType)
    affected_groups = graphene.List(GroupType)
    substitutions = graphene.List(SubstitutionType)


class Query(graphene.ObjectType):
    timetable_teachers = graphene.List(TimetablePersonType)
    timetable_groups = graphene.List(TimetableGroupType)
    timetable_rooms = graphene.List(TimetableRoomType)
    available_timetables = graphene.List(TimetableObjectType)
    substitutions_for_date = graphene.Field(
        SubstitutionsForDateType,
        date=graphene.Date(),
    )
    timetable_days = graphene.List(graphene.Int)

    amended_lessons_from_absences = FilterOrderList(
        LessonEventType,
        obj_type=graphene.String(required=False),
        obj_id=graphene.ID(required=False),
        date_start=graphene.Date(required=True),
        date_end=graphene.Date(required=True),
        teacher=graphene.ID(required=False),
        incomplete=graphene.Boolean(required=False),
    )

    def resolve_timetable_teachers(self, info, **kwargs):
        return graphene_django_optimizer.query(
            get_teachers(info.context.user, request=info.context), info
        )

    def resolve_timetable_groups(self, info, **kwargs):
        return graphene_django_optimizer.query(
            get_groups(info.context.user, request=info.context), info
        )

    def resolve_timetable_rooms(self, info, **kwargs):
        return graphene_django_optimizer.query(get_rooms(info.context.user), info)

    def resolve_available_timetables(self, info, **kwargs):
        all_timetables = []
        for group in get_groups(info.context.user, request=info.context):
            all_timetables.append(
                TimetableObjectType(
                    id=group.id,
                    name=group.name,
                    short_name=group.short_name,
                    type=TimetableType.GROUP,
                )
            )

        for teacher in get_teachers(info.context.user, request=info.context):
            all_timetables.append(
                TimetableObjectType(
                    id=teacher.id,
                    name=teacher.full_name,
                    short_name=teacher.short_name,
                    type=TimetableType.TEACHER,
                )
            )

        for room in get_rooms(info.context.user):
            all_timetables.append(
                TimetableObjectType(
                    id=room.id, name=room.name, short_name=room.short_name, type=TimetableType.ROOM
                )
            )

        return all_timetables

    def resolve_substitutions_for_date(root, info, date):
        substitutions, affected_teachers, affected_groups = build_substitutions_list(date)
        return SubstitutionsForDateType(
            affected_teachers=affected_teachers,
            affected_groups=affected_groups,
            substitutions=[sub["el"] for sub in substitutions],
        )

    @staticmethod
    def resolve_timetable_days(root, info, **kwargs):
        first_day = "default"

        if has_person(info.context):
            first_day = info.context.user.person.preferences["calendar__first_day_of_the_week"]

        if first_day == "default":
            first_day = get_site_preferences()["calendar__first_day_of_the_week"]

        first_day = int(first_day)

        days = list(map(str, range(7)))
        sorted_days = days[first_day:] + days[:first_day]

        allowed_days = get_site_preferences()["chronos__days_in_calendar"]

        return list(map(int, filter(lambda d: d in allowed_days, sorted_days)))

    def resolve_amended_lessons_from_absences(
        root,
        info,
        date_start,
        date_end,
        obj_type="GROUP",
        obj_id=None,
        teacher=None,
        incomplete=False,
        **kwargs,
    ):
        datetime_start = datetime.combine(date_start, datetime.min.time())
        datetime_end = datetime.combine(date_end, datetime.max.time())

        if (
            obj_id
            and not info.context.user.has_perm(
                "chronos.manage_substitutions_for_group_rule", Group.objects.get(id=obj_id)
            )
        ) or (
            not obj_id and not info.context.user.has_perm("chronos.view_substitution_overview_rule")
        ):
            raise PermissionDenied()

        return LessonEvent.get_for_substitution_overview(
            datetime_start, datetime_end, info.context, obj_type, obj_id, teacher, incomplete
        )


class Mutation(graphene.ObjectType):
    create_amend_lessons = AmendLessonBatchCreateMutation.Field()
    patch_amend_lessons = AmendLessonBatchPatchMutation.Field()
    patch_amend_lessons_with_amends = AmendLessonBatchPatchMutation.Field()
    delete_amend_lessons = AmendLessonBatchDeleteMutation.Field()

    create_or_update_substitutions = SubstitutionBatchCreateOrUpdateMutation.Field()
