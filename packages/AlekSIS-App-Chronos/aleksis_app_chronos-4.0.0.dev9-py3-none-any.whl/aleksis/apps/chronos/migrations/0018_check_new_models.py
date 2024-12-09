from django.db import migrations, models

from django.apps import apps as global_apps

def check_for_migration(apps, schema_editor):
    if global_apps.is_installed('aleksis.apps.lesrooster'):
        return

    ValidityRange = apps.get_model('chronos', 'ValidityRange')
    Subject = apps.get_model('chronos', 'Subject')
    AbsenceReason = apps.get_model('chronos', 'AbsenceReason')
    Absence = apps.get_model('chronos', 'Absence')
    Holiday = apps.get_model('chronos', 'Holiday')
    SupervisionArea = apps.get_model('chronos', 'SupervisionArea')

    model_types = [ValidityRange, Subject, AbsenceReason, Absence, Holiday, SupervisionArea]

    for model in model_types:
        if model.objects.exists():
            raise RuntimeError("You have legacy data. Please install AlekSIS-App-Lesrooster to migrate them.")

class Migration(migrations.Migration):

    dependencies = [
        ('chronos', '0017_optional_slot_number'),
    ]

    operations = [
        migrations.RunPython(check_for_migration),
    ]
