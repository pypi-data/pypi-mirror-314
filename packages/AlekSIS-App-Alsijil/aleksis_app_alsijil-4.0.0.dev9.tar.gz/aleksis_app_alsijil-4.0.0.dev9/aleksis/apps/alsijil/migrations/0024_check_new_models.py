from django.db import migrations, models

from django.apps import apps as global_apps

def check_for_migration(apps, schema_editor):
    if global_apps.is_installed('aleksis.apps.lesrooster'):
        return

    ExcuseType = apps.get_model('alsijil', 'ExcuseType')
    PersonalNote = apps.get_model('alsijil', 'PersonalNote')
    LessonDocumentation = apps.get_model('alsijil', 'LessonDocumentation')

    model_types = [ExcuseType, PersonalNote, LessonDocumentation]

    for model in model_types:
        if model.objects.exists():
            raise RuntimeError("You have legacy data. Please install AlekSIS-App-Lesrooster to migrate them.")

class Migration(migrations.Migration):

    dependencies = [
        ('alsijil', '0023_add_tardiness_and_rework_constraints'),
    ]

    operations = [
        migrations.RunPython(check_for_migration),
    ]
