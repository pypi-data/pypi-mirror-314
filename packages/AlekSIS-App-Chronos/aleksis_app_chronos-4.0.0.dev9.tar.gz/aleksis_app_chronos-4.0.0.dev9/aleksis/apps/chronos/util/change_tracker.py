from django.contrib.contenttypes.models import ContentType
from django.dispatch import Signal, receiver

from celery import shared_task
from reversion.models import Revision


def _get_substitution_models():
    from aleksis.apps.chronos.models import LessonEvent, SupervisionEvent

    return [LessonEvent, SupervisionEvent]


chronos_revision_created = Signal()
substitutions_changed = Signal()
timetable_data_changed = Signal()


@shared_task
def handle_new_revision(revision_pk: int):
    """Handle a new revision in background using Celery."""
    revision = Revision.objects.get(pk=revision_pk)
    if revision.version_set.filter(content_type__app_label="chronos").exists():
        chronos_revision_created.send(sender=revision)


@receiver(chronos_revision_created)
def handle_substitution_change(sender: Revision, **kwargs):
    """Handle the change of a substitution-like object."""
    # Filter versions by substitution-like models
    content_types = ContentType.objects.get_for_models(*_get_substitution_models()).values()
    versions = sender.version_set.filter(content_type__in=content_types)
    if versions:
        substitutions_changed.send(sender=sender, versions=versions)
