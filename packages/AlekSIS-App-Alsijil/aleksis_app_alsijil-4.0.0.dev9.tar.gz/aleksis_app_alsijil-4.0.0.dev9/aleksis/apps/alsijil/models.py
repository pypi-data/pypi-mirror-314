from datetime import datetime
from typing import List, Optional

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.timezone import localdate, localtime, now
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField

from aleksis.apps.alsijil.managers import (
    DocumentationManager,
    GroupRoleAssignmentManager,
    GroupRoleAssignmentQuerySet,
    GroupRoleManager,
    GroupRoleQuerySet,
    ParticipationStatusManager,
)
from aleksis.apps.chronos.models import LessonEvent
from aleksis.apps.cursus.models import Course, Subject
from aleksis.apps.kolego.models import Absence as KolegoAbsence
from aleksis.apps.kolego.models import AbsenceReason
from aleksis.core.data_checks import field_validation_data_check_factory
from aleksis.core.mixins import ExtensibleModel, GlobalPermissionModel
from aleksis.core.models import CalendarEvent, Group, Person
from aleksis.core.util.core_helpers import get_site_preferences
from aleksis.core.util.model_helpers import ICONS


class ExtraMark(ExtensibleModel):
    """A model for extra marks.

    Can be used for lesson-based counting of things (like forgotten homework).
    """

    short_name = models.CharField(max_length=255, unique=True, verbose_name=_("Short name"))
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    colour_fg = ColorField(verbose_name=_("Foreground colour"), blank=True)
    colour_bg = ColorField(verbose_name=_("Background colour"), blank=True)

    show_in_coursebook = models.BooleanField(default=True, verbose_name=_("Show in coursebook"))

    def __str__(self):
        return f"{self.name}"

    @property
    def count_label(self):
        return f"extra_mark_{self.id}_count"

    class Meta:
        ordering = ["short_name"]
        verbose_name = _("Extra mark")
        verbose_name_plural = _("Extra marks")


class Documentation(CalendarEvent):
    """A documentation on teaching content in a freely choosable time frame.

    Non-personal, includes the topic and homework of the lesson.
    """

    # FIXME: DataCheck

    objects = DocumentationManager()

    course = models.ForeignKey(
        Course,
        models.PROTECT,
        related_name="documentations",
        blank=True,
        null=True,
        verbose_name=_("Course"),
    )

    subject = models.ForeignKey(
        Subject, models.PROTECT, related_name="+", blank=True, null=True, verbose_name=_("Subject")
    )

    teachers = models.ManyToManyField(
        "core.Person",
        related_name="documentations_as_teacher",
        blank=True,
        null=True,
        verbose_name=_("Teachers"),
    )

    topic = models.CharField(verbose_name=_("Lesson Topic"), max_length=255, blank=True)
    homework = models.CharField(verbose_name=_("Homework"), max_length=255, blank=True)
    group_note = models.CharField(verbose_name=_("Group Note"), max_length=255, blank=True)

    # Used to track whether participations have been filled in
    participation_touched_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Participation touched at")
    )

    def get_subject(self) -> str:
        if self.subject:
            return self.subject
        if self.amends:
            if self.amends.subject:
                return self.amends.subject
            if self.amends.course:
                return self.amends.course.subject
        if self.course:
            return self.course.subject

    def get_groups(self) -> QuerySet[Group]:
        if self.amends:
            return self.amends.actual_groups
        if self.course:
            return self.course.groups.all()

    def get_teachers_short_names(self) -> List[str]:
        return [teacher.short_name or teacher.name for teacher in self.teachers.all()]

    def __str__(self) -> str:
        start_datetime = CalendarEvent.value_start_datetime(self)
        end_datetime = CalendarEvent.value_end_datetime(self)
        return (
            f"{','.join([str(g) for g in self.get_groups()])} {self.get_subject()}"
            + f" {start_datetime} - {end_datetime}"
        )

    class Meta:
        verbose_name = _("Documentation")
        verbose_name_plural = _("Documentations")
        # should check if object has either course or amends,
        # which is not possible via constraint, because amends is not local to Documentation

    @classmethod
    def get_documentations_for_events(
        cls,
        datetime_start: datetime,
        datetime_end: datetime,
        events: list,
        incomplete: Optional[bool] = False,
        absences_exist: Optional[bool] = False,
    ) -> tuple:
        """Get all the documentations for the events.
        Create dummy documentations if none exist.
        Returns a tuple with a list of existing documentations and a list dummy documentations.
        """
        docs = []
        dummies = []

        # Prefetch existing documentations to speed things up
        existing_documentations = (
            Documentation.objects.filter(
                datetime_start__lte=datetime_end,
                datetime_end__gte=datetime_start,
                amends__in=[e["REFERENCE_OBJECT"] for e in events],
            )
            .prefetch_related(
                "participations",
                "participations__person",
                "participations__absence_reason",
                "teachers",
                "personal_notes",
                "personal_notes__extra_mark",
            )
            .select_related("course", "subject")
        )

        for event in events:
            if incomplete and event["STATUS"] == "CANCELLED":
                continue

            event_reference_obj = event["REFERENCE_OBJECT"]
            existing_documentations_event = filter(
                lambda d: (
                    d.datetime_start == event["DTSTART"].dt
                    and d.datetime_end == event["DTEND"].dt
                    and d.amends.id == event_reference_obj.id
                ),
                existing_documentations,
            )

            doc = next(existing_documentations_event, None)
            if doc:
                if (incomplete and doc.topic) or (
                    absences_exist
                    and (
                        not doc.participations.all()
                        or not [d for d in doc.participations.all() if d.absence_reason]
                    )
                ):
                    continue
                doc._amends_prefetched = event_reference_obj
                docs.append(doc)
            elif not absences_exist:
                if event_reference_obj.amends:
                    if event_reference_obj.course:
                        course = event_reference_obj.course
                    else:
                        course = event_reference_obj.amends.course

                    if event_reference_obj.subject:
                        subject = event_reference_obj.subject
                    else:
                        subject = event_reference_obj.amends.subject
                else:
                    course, subject = event_reference_obj.course, event_reference_obj.subject

                dummies.append(
                    cls(
                        pk=f"DUMMY;{event_reference_obj.id};{event['DTSTART'].dt.isoformat()};{event['DTEND'].dt.isoformat()}",
                        amends=event_reference_obj,
                        course=course,
                        subject=subject,
                        datetime_start=event["DTSTART"].dt,
                        datetime_end=event["DTEND"].dt,
                    )
                )

        return docs, dummies

    @classmethod
    def get_documentations_for_person(
        cls,
        person: int,
        start: datetime,
        end: datetime,
        incomplete: Optional[bool] = False,
    ) -> tuple:
        """Get all the documentations for the person from start to end datetime.
        Create dummy documentations if none exist.
        Returns a tuple with a list of existing documentations and a list dummy documentations.
        """
        event_params = {
            "type": "PARTICIPANT",
            "id": person,
        }

        events = LessonEvent.get_single_events(
            start,
            end,
            None,
            event_params,
            with_reference_object=True,
        )

        return Documentation.get_documentations_for_events(start, end, events, incomplete)

    @classmethod
    def parse_dummy(
        cls,
        _id: str,
    ) -> tuple:
        """Parse dummy id string into lesson_event, datetime_start, datetime_end."""
        dummy, lesson_event_id, datetime_start_iso, datetime_end_iso = _id.split(";")
        lesson_event = LessonEvent.objects.get(id=lesson_event_id)

        datetime_start = datetime.fromisoformat(datetime_start_iso).astimezone(
            lesson_event.timezone
        )
        datetime_end = datetime.fromisoformat(datetime_end_iso).astimezone(lesson_event.timezone)
        return (lesson_event, datetime_start, datetime_end)

    @classmethod
    def create_from_lesson_event(
        cls,
        user: User,
        lesson_event: LessonEvent,
        datetime_start: datetime,
        datetime_end: datetime,
    ) -> "Documentation":
        """Create a documentation from a lesson_event with start and end datetime.
        User is needed for permission checking.
        """
        if not user.has_perm(
            "alsijil.add_documentation_for_lesson_event_rule", lesson_event
        ) or not (
            get_site_preferences()["alsijil__allow_edit_future_documentations"] == "all"
            or (
                get_site_preferences()["alsijil__allow_edit_future_documentations"] == "current_day"
                and datetime_start.date() <= localdate()
            )
            or (
                get_site_preferences()["alsijil__allow_edit_future_documentations"]
                == "current_time"
                and datetime_start <= localtime()
            )
        ):
            raise PermissionDenied()

        if lesson_event.amends:
            course = lesson_event.course if lesson_event.course else lesson_event.amends.course

            subject = lesson_event.subject if lesson_event.subject else lesson_event.amends.subject

            teachers = (
                lesson_event.teachers if lesson_event.teachers else lesson_event.amends.teachers
            )
        else:
            course, subject, teachers = (
                lesson_event.course,
                lesson_event.subject,
                lesson_event.teachers,
            )

        obj, __ = cls.objects.update_or_create(
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            amends=lesson_event,
            defaults=dict(subject=subject, course=course),
        )
        obj.teachers.set(teachers.all())

        # Create Participation Statuses
        obj.touch()

        return obj

    @classmethod
    def get_or_create_by_id(cls, _id: str, user):
        if _id.startswith("DUMMY"):
            return cls.create_from_lesson_event(
                user,
                *cls.parse_dummy(_id),
            ), True

        obj = cls.objects.get(id=_id)
        if not user.has_perm("alsijil.edit_documentation_rule", obj):
            raise PermissionDenied()
        return obj, False

    def touch(self):
        """Ensure that participation statuses are created for this documentation."""
        if (
            self.participation_touched_at
            or not self.amends
            or self.value_start_datetime(self) > now()
            or self.amends.cancelled
        ):
            # There is no source to update from or it's too early
            return

        lesson_event: LessonEvent = self.amends
        all_members = lesson_event.all_members
        member_pks = [p.pk for p in all_members]

        new_persons = Person.objects.filter(Q(pk__in=member_pks)).prefetch_related("member_of")

        # Get absences from Kolego
        events = KolegoAbsence.get_single_events(
            self.value_start_datetime(self),
            self.value_end_datetime(self),
            None,
            {"persons": member_pks},
            with_reference_object=True,
        )
        kolego_absences_map = {a["REFERENCE_OBJECT"].person: a["REFERENCE_OBJECT"] for a in events}

        new_participations = []
        new_groups_of_person = []
        for person in new_persons:
            participation_status = ParticipationStatus(
                person=person,
                related_documentation=self,
                datetime_start=self.datetime_start,
                datetime_end=self.datetime_end,
                timezone=self.timezone,
            )

            # Take over data from Kolego absence
            if person in kolego_absences_map:
                participation_status.fill_from_kolego(kolego_absences_map[person])

            participation_status.save()

            new_groups_of_person += [
                ParticipationStatus.groups_of_person.through(
                    group=group, participationstatus=participation_status
                )
                for group in person.member_of.all()
            ]
            new_participations.append(participation_status)
        ParticipationStatus.groups_of_person.through.objects.bulk_create(new_groups_of_person)

        self.participation_touched_at = timezone.now()
        self.save()

        return new_participations


class ParticipationStatus(CalendarEvent):
    """A participation or absence record about a single person.

    Used in the class register to note participation or absence of a student
    in a documented unit (e.g. a single lesson event or a custom time frame; see Documentation).
    """

    # FIXME: DataChecks

    objects = ParticipationStatusManager()

    person = models.ForeignKey(
        "core.Person", models.CASCADE, related_name="participations", verbose_name=_("Person")
    )
    groups_of_person = models.ManyToManyField(
        "core.Group", related_name="+", verbose_name=_("Groups of Person")
    )

    related_documentation = models.ForeignKey(
        Documentation,
        models.CASCADE,
        related_name="participations",
        verbose_name=_("Documentation"),
    )

    # Absence part
    absence_reason = models.ForeignKey(
        AbsenceReason,
        verbose_name=_("Absence Reason"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    base_absence = models.ForeignKey(
        KolegoAbsence,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="absences",
        verbose_name=_("Base Absence"),
    )

    tardiness = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("Tardiness"))

    @classmethod
    def get_objects(
        cls,
        request: HttpRequest | None = None,
        params: dict[str, any] | None = None,
        additional_filter: Q | None = None,
        **kwargs,
    ) -> QuerySet:
        q = additional_filter or Q()
        if params:
            if params.get("person"):
                q = q & Q(person=params["person"])
            elif params.get("persons"):
                q = q & Q(person__in=params["persons"])
            elif params.get("group"):
                q = q & Q(groups_of_person__in=params.get("group"))
        qs = super().get_objects(
            request,
            params,
            additional_filter=q,
            select_related=["person", "absence_reason"],
            **kwargs,
        )

        return qs

    @classmethod
    def value_title(
        cls, reference_object: "ParticipationStatus", request: HttpRequest | None = None
    ) -> str:
        """Return the title of the calendar event."""
        return f"{reference_object.person} ({reference_object.absence_reason})"

    @classmethod
    def value_description(
        cls, reference_object: "ParticipationStatus", request: HttpRequest | None = None
    ) -> str:
        """Return the title of the calendar event."""
        return ""

    @classmethod
    def set_from_kolego_by_datetimes(
        cls, kolego_absence: KolegoAbsence, person: Person, start: datetime, end: datetime
    ) -> list["ParticipationStatus"]:
        participation_statuses = []

        events = cls.get_single_events(
            start,
            end,
            None,
            {"person": person},
            with_reference_object=True,
        )

        for event in events:
            participation_status = event["REFERENCE_OBJECT"]
            participation_status.absence_reason = kolego_absence.reason
            participation_status.base_absence = kolego_absence
            participation_status.save()
            participation_statuses.append(participation_status)

        return participation_statuses

    def fill_from_kolego(self, kolego_absence: KolegoAbsence):
        """Take over data from a Kolego absence."""
        self.base_absence = kolego_absence
        self.absence_reason = kolego_absence.reason

    def __str__(self) -> str:
        return f"{self.related_documentation.id}, {self.person}"

    class Meta:
        verbose_name = _("Participation Status")
        verbose_name_plural = _("Participation Status")
        ordering = [
            "related_documentation",
            "person__last_name",
            "person__first_name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("related_documentation", "person"),
                name="unique_participation_status_per_documentation",
            ),
        ]


class NewPersonalNote(ExtensibleModel):
    person = models.ForeignKey(
        "core.Person", models.CASCADE, related_name="new_personal_notes", verbose_name=_("Person")
    )

    documentation = models.ForeignKey(
        Documentation,
        models.CASCADE,
        related_name="personal_notes",
        verbose_name=_("Documentation"),
        blank=True,
        null=True,
    )

    note = models.TextField(blank=True, default="", verbose_name=_("Note"))
    extra_mark = models.ForeignKey(
        ExtraMark, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_("Extra Mark")
    )

    def __str__(self) -> str:
        return f"{self.person}, {self.note}, {self.extra_mark}"

    class Meta:
        verbose_name = _("Personal Note")
        verbose_name_plural = _("Personal Notes")
        constraints = [
            # This constraint could be dropped in future scenarios
            models.CheckConstraint(
                check=~Q(note="") | Q(extra_mark__isnull=False),
                name="either_note_or_extra_mark_per_note",
            ),
            models.UniqueConstraint(
                fields=["person", "documentation", "extra_mark"],
                name="unique_person_documentation_extra_mark",
                violation_error_message=_(
                    "A person got assigned the same extra mark multiple times per documentation."
                ),
                condition=~Q(extra_mark=None),
            ),
        ]


class GroupRole(ExtensibleModel):
    data_checks = [field_validation_data_check_factory("alsijil", "GroupRole", "icon")]

    objects = GroupRoleManager.from_queryset(GroupRoleQuerySet)()

    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    icon = models.CharField(max_length=50, blank=True, choices=ICONS, verbose_name=_("Icon"))
    colour = ColorField(blank=True, verbose_name=_("Colour"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Group role")
        verbose_name_plural = _("Group roles")
        permissions = (("assign_group_role", _("Can assign group role")),)

    def get_absolute_url(self) -> str:
        return reverse("edit_group_role", args=[self.id])


class GroupRoleAssignment(ExtensibleModel):
    objects = GroupRoleAssignmentManager.from_queryset(GroupRoleAssignmentQuerySet)()

    role = models.ForeignKey(
        GroupRole,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name=_("Group role"),
    )
    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="group_roles",
        verbose_name=_("Assigned person"),
    )
    groups = models.ManyToManyField(
        "core.Group",
        related_name="group_roles",
        verbose_name=_("Groups"),
    )
    date_start = models.DateField(verbose_name=_("Start date"))
    date_end = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("End date"),
        help_text=_("Can be left empty if end date is not clear yet"),
    )

    def __str__(self):
        date_end = date_format(self.date_end) if self.date_end else "?"
        return f"{self.role}: {self.person}, {date_format(self.date_start)}–{date_end}"

    @property
    def date_range(self) -> str:
        if not self.date_end:
            return f"{date_format(self.date_start)}–?"
        else:
            return f"{date_format(self.date_start)}–{date_format(self.date_end)}"

    class Meta:
        verbose_name = _("Group role assignment")
        verbose_name_plural = _("Group role assignments")


class AlsijilGlobalPermissions(GlobalPermissionModel):
    class Meta:
        managed = False
        permissions = (
            ("view_lesson", _("Can view lesson overview")),
            ("view_week", _("Can view week overview")),
            ("view_full_register", _("Can view full register")),
            ("register_absence", _("Can register absence")),
            ("list_personal_note_filters", _("Can list all personal note filters")),
        )
