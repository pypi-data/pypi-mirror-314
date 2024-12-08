from datetime import date
from typing import List, Optional

from django.db.models import Prefetch, Q
from django.utils.translation import gettext as _

from celery.result import allow_join_result
from celery.states import SUCCESS

from aleksis.apps.cursus.models import Course
from aleksis.apps.kolego.models.absence import AbsenceReason
from aleksis.core.models import Group, PDFFile
from aleksis.core.util.celery_progress import ProgressRecorder, recorded_task
from aleksis.core.util.pdf import generate_pdf_from_template

from .model_extensions import annotate_person_statistics_from_documentations
from .models import Documentation, ExtraMark, NewPersonalNote, ParticipationStatus


@recorded_task
def generate_full_register_printout(
    groups: List[int],
    file_object: int,
    recorder: ProgressRecorder,
    include_cover: Optional[bool] = True,
    include_abbreviations: Optional[bool] = True,
    include_members_table: Optional[bool] = True,
    include_teachers_and_subjects_table: Optional[bool] = True,
    include_person_overviews: Optional[bool] = True,
    include_coursebook: Optional[bool] = True,
):
    """Generate a configurable register printout as PDF for a group."""

    def prefetch_notable_participations(select_related=None, prefetch_related=None):
        if not select_related:
            select_related = []
        if not prefetch_related:
            prefetch_related = []
        return Prefetch(
            "participations",
            to_attr="notable_participations",
            queryset=ParticipationStatus.objects.filter(
                Q(absence_reason__tags__short_name="class_register") | Q(tardiness__isnull=False)
            )
            .select_related("absence_reason", *select_related)
            .prefetch_related(*prefetch_related),
        )

    def prefetch_personal_notes(name, select_related=None, prefetch_related=None):
        if not select_related:
            select_related = []
        if not prefetch_related:
            prefetch_related = []
        return Prefetch(
            name,
            queryset=NewPersonalNote.objects.filter(Q(note__gt="") | Q(extra_mark__isnull=False))
            .select_related("extra_mark", *select_related)
            .prefetch_related(*prefetch_related),
        )

    context = {}

    context["include_cover"] = include_cover
    context["include_abbreviations"] = include_abbreviations
    context["include_members_table"] = include_members_table
    context["include_teachers_and_subjects_table"] = include_teachers_and_subjects_table
    context["include_person_overviews"] = include_person_overviews
    context["include_coursebook"] = include_coursebook

    context["today"] = date.today()

    _number_of_steps = 5 + len(groups)

    recorder.set_progress(1, _number_of_steps, _("Loading data ..."))

    groups = Group.objects.filter(pk__in=groups).order_by("name")

    if include_cover:
        groups = groups.select_related("school_term")

    if include_abbreviations or include_members_table:
        context["absence_reasons"] = AbsenceReason.objects.filter(
            tags__short_name="class_register", count_as_absent=True
        )
        context["absence_reasons_not_counted"] = AbsenceReason.objects.filter(
            tags__short_name="class_register", count_as_absent=False
        )
        context["extra_marks"] = ExtraMark.objects.all()

    if include_members_table or include_person_overviews:
        groups = groups.prefetch_related("members")

    if include_teachers_and_subjects_table:
        groups = groups.prefetch_related(
            Prefetch("courses", queryset=Course.objects.select_related("subject")),
            "courses__teachers",
            "child_groups",
            Prefetch("child_groups__courses", queryset=Course.objects.select_related("subject")),
            "child_groups__courses__teachers",
        )

    recorder.set_progress(2, _number_of_steps, _("Loading groups ..."))

    for i, group in enumerate(groups, start=1):
        recorder.set_progress(
            2 + i, _number_of_steps, _(f"Loading group {group.short_name or group.name} ...")
        )

        if include_members_table or include_person_overviews or include_coursebook:
            documentations = Documentation.objects.filter(
                Q(datetime_start__date__gte=group.school_term.date_start)
                & Q(datetime_end__date__lte=group.school_term.date_end)
                & Q(
                    pk__in=Documentation.objects.filter(course__groups=group)
                    .values_list("pk", flat=True)
                    .union(
                        Documentation.objects.filter(
                            course__groups__parent_groups=group
                        ).values_list("pk", flat=True)
                    )
                )
            )

        if include_members_table or include_person_overviews:
            group.members_with_stats = annotate_person_statistics_from_documentations(
                group.members.all(), documentations
            )

        if include_person_overviews:
            doc_query_set = documentations.select_related("subject").prefetch_related("teachers")
            group.members_with_stats = group.members_with_stats.prefetch_related(
                prefetch_notable_participations(
                    prefetch_related=[Prefetch("related_documentation", queryset=doc_query_set)]
                ),
                prefetch_personal_notes(
                    "new_personal_notes",
                    prefetch_related=[Prefetch("documentation", queryset=doc_query_set)],
                ),
            )

        if include_teachers_and_subjects_table:
            group.as_list = [group]

        if include_coursebook:
            group.documentations = documentations.order_by(
                "datetime_start"
            ).prefetch_related(
                prefetch_notable_participations(select_related=["person"]),
                prefetch_personal_notes("personal_notes", select_related=["person"]),
            )

    context["groups"] = groups

    recorder.set_progress(3 + len(groups), _number_of_steps, _("Generating template ..."))

    file_object, result = generate_pdf_from_template(
        "alsijil/print/register_for_group.html",
        context,
        file_object=PDFFile.objects.get(pk=file_object),
    )

    recorder.set_progress(4 + len(groups), _number_of_steps, _("Generating PDF ..."))

    with allow_join_result():
        result.wait()
        file_object.refresh_from_db()
        if not result.status == SUCCESS and file_object.file:
            raise Exception(_("PDF generation failed"))

    recorder.set_progress(5 + len(groups), _number_of_steps)
