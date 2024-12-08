import datetime

from django.core.exceptions import PermissionDenied
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _

import graphene
from graphene_django import DjangoObjectType
from reversion import create_revision, set_comment, set_user

from aleksis.apps.alsijil.models import NewPersonalNote, ParticipationStatus
from aleksis.apps.alsijil.schema.personal_note import PersonalNoteType
from aleksis.apps.kolego.models import Absence
from aleksis.apps.kolego.schema.absence import AbsenceType
from aleksis.core.schema.base import (
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
)


class ParticipationStatusType(
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
    DjangoFilterMixin,
    DjangoObjectType,
):
    class Meta:
        model = ParticipationStatus
        fields = (
            "id",
            "person",
            "absence_reason",
            "related_documentation",
            "base_absence",
            "tardiness",
        )

    notes_with_extra_mark = graphene.List(PersonalNoteType)
    notes_with_note = graphene.List(PersonalNoteType)

    @staticmethod
    def resolve_notes_with_extra_mark(root: ParticipationStatus, info, **kwargs):
        if hasattr(root, "_prefetched_documentation"):
            return [
                p
                for p in root._prefetched_documentation.personal_notes.all()
                if p.person_id == root.person_id and p.extra_mark
            ]
        return NewPersonalNote.objects.filter(
            person=root.person,
            documentation=root.related_documentation,
            extra_mark__isnull=False,
        )

    @staticmethod
    def resolve_notes_with_note(root: ParticipationStatus, info, **kwargs):
        if hasattr(root, "_prefetched_documentation"):
            return [
                p
                for p in root._prefetched_documentation.personal_notes.all()
                if p.person_id == root.person_id and p.note
            ]
        return NewPersonalNote.objects.filter(
            person=root.person,
            documentation=root.related_documentation,
            note__isnull=False,
        ).exclude(note="")


class ParticipationStatusBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = ParticipationStatus
        fields = (
            "id",
            "absence_reason",
            "tardiness",
        )  # Only the reason and tardiness can be updated after creation
        return_field_name = "participationStatuses"

    @classmethod
    def check_permissions(cls, root, info, input, *args, **kwargs):  # noqa: A002
        pass

    @classmethod
    def after_update_obj(cls, root, info, input, obj, full_input):  # noqa: A002
        if not info.context.user.has_perm(
            "alsijil.edit_participation_status_for_documentation_with_time_range_rule",
            obj.related_documentation,
        ):
            raise PermissionDenied()


class ExtendParticipationStatusToAbsenceBatchMutation(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.ID, description=_("List of ParticipationStatus IDs"))

    participations = graphene.List(ParticipationStatusType)
    absences = graphene.List(AbsenceType)

    @classmethod
    def create_absence(cls, info, participation_id):
        participation = ParticipationStatus.objects.get(pk=participation_id)

        if participation.date_end:
            end_date = participation.date_end
        else:
            end_date = participation.datetime_end.date()

        end_datetime = datetime.datetime.combine(
            end_date, datetime.time.max, participation.timezone
        )

        data = dict(
            reason=participation.absence_reason if participation.absence_reason else None,
            person=participation.person,
        )

        if participation.date_start:
            data["date_start"] = participation.date_start
            data["date_end"] = end_date
            start_datetime = datetime.datetime.combine(
                participation.date_start, datetime.time.min, participation.timezone
            )
        else:
            data["datetime_start"] = participation.datetime_start
            data["datetime_end"] = end_datetime
            start_datetime = participation.datetime_start

        defaults = dict(
            comment=_("Extended by {full_name} on {datetime}").format(
                full_name=info.context.user.person.full_name,
                datetime=date_format(participation.date_start or participation.datetime_start),
            )
        )

        absence = Absence.get_for_person_by_datetimes(**data, defaults=defaults)

        participations = ParticipationStatus.set_from_kolego_by_datetimes(
            kolego_absence=absence,
            person=participation.person,
            start=start_datetime,
            end=end_datetime,
        )

        return participations, absence

    @classmethod
    def mutate(cls, root, info, input):  # noqa
        with create_revision():
            set_user(info.context.user)
            set_comment(_("Extended absence reason from coursebook."))
            participations = []
            absences = []
            for participation_id in input:
                p, a = cls.create_absence(info, participation_id)
                participations += p
                absences.append(a)

        return ExtendParticipationStatusToAbsenceBatchMutation(
            participations=participations, absences=absences
        )
