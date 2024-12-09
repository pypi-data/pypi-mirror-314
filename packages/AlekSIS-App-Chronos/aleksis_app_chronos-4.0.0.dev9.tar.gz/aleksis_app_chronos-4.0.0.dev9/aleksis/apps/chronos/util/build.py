from datetime import date, datetime, time

from aleksis.apps.chronos.models import LessonEvent, SupervisionEvent
from aleksis.core.models import Group, Person


def build_substitutions_list(wanted_day: date) -> tuple[list[dict], list[Person], list[Group]]:
    rows = []
    affected_teachers = set()
    affected_groups = set()

    lesson_events = LessonEvent.get_single_events(
        datetime.combine(wanted_day, time.min),
        datetime.combine(wanted_day, time.max),
        params={"current_changes": True},
        with_reference_object=True,
    )

    for lesson_event in lesson_events:
        ref_object = lesson_event["REFERENCE_OBJECT"]
        affected_teachers.update(lesson_event["REFERENCE_OBJECT"].teachers.all())
        affected_groups.update(lesson_event["REFERENCE_OBJECT"].groups.all())
        if ref_object.amends:
            affected_teachers.update(ref_object.amends.teachers.all())
            affected_groups.update(ref_object.amends.groups.all())

        row = {
            "type": "substitution",
            "sort_a": ref_object.group_names,
            "sort_b": str(lesson_event["DTSTART"]),
            "el": lesson_event,
        }

        rows.append(row)

    supervision_events = SupervisionEvent.get_single_events(
        datetime.combine(wanted_day, time.min),
        datetime.combine(wanted_day, time.max),
        params={"current_changes": True},
        with_reference_object=True,
    )

    for supervision_event in supervision_events:
        ref_object = supervision_event["REFERENCE_OBJECT"]
        affected_teachers.update(ref_object.teachers.all())
        if ref_object.amends:
            affected_teachers.update(ref_object.amends.teachers.all())

        row = {
            "type": "supervision_substitution",
            "sort_a": "Z",
            "sort_b": str(supervision_event["DTSTART"]),
            "el": supervision_event,
        }

        rows.append(row)

    rows.sort(key=lambda row: row["sort_a"] + row["sort_b"])

    affected_teachers = sorted(affected_teachers, key=lambda p: p.short_name or p.last_name)
    affected_groups = sorted(affected_groups, key=lambda g: g.short_name or g.name)

    return rows, affected_teachers, affected_groups
