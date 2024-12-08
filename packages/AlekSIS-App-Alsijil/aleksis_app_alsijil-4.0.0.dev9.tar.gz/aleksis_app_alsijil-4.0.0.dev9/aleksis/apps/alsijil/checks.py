import logging
from datetime import datetime, time
from typing import TYPE_CHECKING

from django.db.models.query_utils import Q
from django.utils.translation import gettext as _

from aleksis.apps.chronos.models import LessonEvent
from aleksis.core.data_checks import DataCheck, IgnoreSolveOption, SolveOption

if TYPE_CHECKING:
    from aleksis.core.models import DataCheckResult


class DeleteRelatedObjectSolveOption(SolveOption):
    name = "delete"
    verbose_name = _("Delete object")

    @classmethod
    def solve(cls, check_result: "DataCheckResult"):
        check_result.related_object.delete()
        check_result.delete()


class SetGroupsWithCurrentGroupsSolveOption(SolveOption):
    name = "set_groups_of_person"
    verbose_name = _("Set current groups")

    @classmethod
    def solve(cls, check_result: "DataCheckResult"):
        person = check_result.related_object.person
        check_result.related_object.groups_of_person.set(person.member_of.all())
        check_result.delete()


class NoParticipationStatusesPersonalNotesInCancelledLessonsDataCheck(DataCheck):
    name = "no_personal_notes_participation_statuses_in_cancelled_lessons"
    verbose_name = _(
        "Ensure that there are no participation statuses and personal notes in cancelled lessons"
    )
    problem_name = _("The participation status or personal note is related to a cancelled lesson.")
    solve_options = {
        DeleteRelatedObjectSolveOption.name: DeleteRelatedObjectSolveOption,
        IgnoreSolveOption.name: IgnoreSolveOption,
    }

    @classmethod
    def check_data(cls):
        from .models import NewPersonalNote, ParticipationStatus

        participation_statuses = ParticipationStatus.objects.filter(
            related_documentation__amends__in=LessonEvent.objects.filter(cancelled=True)
        )
        personal_notes = NewPersonalNote.objects.filter(
            documentation__amends__in=LessonEvent.objects.filter(cancelled=True)
        )

        for status in participation_statuses:
            logging.info(f"Check participation status {status}")
            cls.register_result(status)

        for note in personal_notes:
            logging.info(f"Check personal note {note}")
            cls.register_result(note)


class NoGroupsOfPersonsSetInParticipationStatusesDataCheck(DataCheck):
    name = "no_groups_of_persons_set_in_participation_statuses"
    verbose_name = _("Ensure that 'groups_of_person' is set for every participation status")
    problem_name = _("The participation status has no group in 'groups_of_person'.")
    solve_options = {
        SetGroupsWithCurrentGroupsSolveOption.name: SetGroupsWithCurrentGroupsSolveOption,
        DeleteRelatedObjectSolveOption.name: DeleteRelatedObjectSolveOption,
        IgnoreSolveOption.name: IgnoreSolveOption,
    }

    @classmethod
    def check_data(cls):
        from .models import ParticipationStatus

        participation_statuses = ParticipationStatus.objects.filter(groups_of_person__isnull=True)

        for status in participation_statuses:
            logging.info(f"Check participation status {status}")
            cls.register_result(status)


class DocumentationOnHolidaysDataCheck(DataCheck):
    """Checks for documentation objects on holidays."""

    name = "documentation_on_holidays"
    verbose_name = _("Ensure that there are no documentations on holidays")
    problem_name = _("The documentation is on holidays.")
    solve_options = {
        DeleteRelatedObjectSolveOption.name: DeleteRelatedObjectSolveOption,
        IgnoreSolveOption.name: IgnoreSolveOption,
    }

    @classmethod
    def check_data(cls):
        from aleksis.core.models import Holiday

        from .models import Documentation

        holidays = Holiday.objects.all()

        q = Q(pk__in=[])
        for holiday in holidays:
            q = q | Q(
                datetime_start__gte=datetime.combine(holiday.date_start, time.min),
                datetime_end__lte=datetime.combine(holiday.date_end, time.max),
            )
        documentations = Documentation.objects.filter(q)

        for doc in documentations:
            logging.info(f"Documentation {doc} is on holidays")
            cls.register_result(doc)


class ParticipationStatusPersonalNoteOnHolidaysDataCheck(DataCheck):
    """Checks for participation status and personal note objects on holidays."""

    name = "participation_status_personal_note_on_holidays"
    verbose_name = _(
        "Ensure that there are no participation statuses or personal notes on holidays"
    )
    problem_name = _("The participation status or personal note is on holidays.")
    solve_options = {
        DeleteRelatedObjectSolveOption.name: DeleteRelatedObjectSolveOption,
        IgnoreSolveOption.name: IgnoreSolveOption,
    }

    @classmethod
    def check_data(cls):
        from aleksis.core.models import Holiday

        from .models import ParticipationStatus

        holidays = Holiday.objects.all()

        q = Q(pk__in=[])
        for holiday in holidays:
            q = q | Q(
                datetime_start__gte=datetime.combine(holiday.date_start, time.min),
                datetime_end__lte=datetime.combine(holiday.date_end, time.max),
            )

        participation_statuses = ParticipationStatus.objects.filter(q)

        for status in participation_statuses:
            logging.info(f"Participation status {status} is on holidays")
            cls.register_result(status)
