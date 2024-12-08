from aleksis.apps.kolego.models import AbsenceReasonTag


def get_absence_reason_tag():
    return AbsenceReasonTag.objects.managed_by_app("alsijil").get_or_create(
        managed_by_app_label="alsijil",
        short_name="class_register",
        defaults={"name": "Class Register"},
    )
