# Generated by Django 3.2.4 on 2021-08-29 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alsijil', '0014_fix_unique_lesson_documentation'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='personalnote',
            name='unique_personal_note_per_object',
        ),
        migrations.AddConstraint(
            model_name='personalnote',
            constraint=models.UniqueConstraint(fields=('week', 'year', 'lesson_period', 'person'), name='unique_note_per_lp'),
        ),
        migrations.AddConstraint(
            model_name='personalnote',
            constraint=models.UniqueConstraint(fields=('week', 'year', 'event', 'person'), name='unique_note_per_ev'),
        ),
        migrations.AddConstraint(
            model_name='personalnote',
            constraint=models.UniqueConstraint(fields=('week', 'year', 'extra_lesson', 'person'), name='unique_note_per_el'),
        ),
    ]
