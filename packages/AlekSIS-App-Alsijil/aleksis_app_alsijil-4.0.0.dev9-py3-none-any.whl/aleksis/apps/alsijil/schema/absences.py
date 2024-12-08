import datetime
from typing import List

from django.core.exceptions import PermissionDenied

import graphene

from aleksis.apps.kolego.models import Absence
from aleksis.core.models import Person

from ..models import ParticipationStatus
from .participation_status import ParticipationStatusType


class AbsencesForPersonsCreateMutation(graphene.Mutation):
    class Arguments:
        persons = graphene.List(graphene.ID, required=True)
        start = graphene.DateTime(required=True)
        end = graphene.DateTime(required=True)
        comment = graphene.String(required=False)
        reason = graphene.ID(required=True)

    ok = graphene.Boolean()
    participation_statuses = graphene.List(ParticipationStatusType)

    @classmethod
    def mutate(
        cls,
        root,
        info,
        persons: List[str | int],
        start: datetime.datetime,
        end: datetime.datetime,
        comment: str,
        reason: str | int,
    ):
        participation_statuses = []

        persons = Person.objects.filter(pk__in=persons)

        for person in persons:
            if not info.context.user.has_perm("alsijil.register_absence_rule", person):
                raise PermissionDenied()

            kolego_absence = Absence.get_for_person_by_datetimes(
                datetime_start=start,
                datetime_end=end,
                reason_id=reason,
                person=person,
                defaults={"comment": comment},
            )

            participation_statuses += ParticipationStatus.set_from_kolego_by_datetimes(
                kolego_absence=kolego_absence, person=person, start=start, end=end
            )

        return AbsencesForPersonsCreateMutation(
            ok=True, participation_statuses=participation_statuses
        )
