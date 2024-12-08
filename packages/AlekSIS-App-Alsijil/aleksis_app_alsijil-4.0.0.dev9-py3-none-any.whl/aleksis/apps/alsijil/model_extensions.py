from django.db.models import FilteredRelation, Q, QuerySet, Value
from django.db.models.aggregates import Count, Sum
from django.utils.translation import gettext as _

from aleksis.apps.kolego.models import AbsenceReason
from aleksis.core.models import Group, Person, SchoolTerm

from .models import Documentation, ExtraMark

# Dynamically add extra permissions to Group and Person models in core
# Note: requires migrate afterwards
Group.add_permission(
    "view_week_class_register_group",
    _("Can view week overview of group class register"),
)
Group.add_permission(
    "view_lesson_class_register_group",
    _("Can view lesson overview of group class register"),
)
Group.add_permission("view_personalnote_group", _("Can view all personal notes of a group"))
Group.add_permission("edit_personalnote_group", _("Can edit all personal notes of a group"))
Group.add_permission(
    "view_lessondocumentation_group", _("Can view all lesson documentation of a group")
)
Group.add_permission(
    "edit_lessondocumentation_group", _("Can edit all lesson documentation of a group")
)
Group.add_permission("view_full_register_group", _("Can view full register of a group"))
Group.add_permission(
    "register_absence_group", _("Can register an absence for all members of a group")
)
Group.add_permission("assign_grouprole", _("Can assign a group role for this group"))
Person.add_permission("register_absence_person", _("Can register an absence for a person"))


def annotate_person_statistics(
    persons: QuerySet[Person],
    participations_filter: Q,
    personal_notes_filter: Q,
    *,
    ignore_filters: bool = False,
) -> QuerySet[Person]:
    """Annotate a queryset of persons with class register statistics."""

    if ignore_filters:
        persons = persons.annotate(
            absence_count=Value(0),
            filtered_participation_statuses=FilteredRelation(
                "participations",
                condition=Q(pk=None),
            ),
            filtered_personal_notes=FilteredRelation(
                "new_personal_notes",
                condition=Q(pk=None),
            ),
            participation_count=Value(0),
            tardiness_count=Value(0),
            tardiness_sum=Value(0),
        )
    else:
        persons = persons.annotate(
            filtered_participation_statuses=FilteredRelation(
                "participations",
                condition=(participations_filter),
            ),
            filtered_personal_notes=FilteredRelation(
                "new_personal_notes",
                condition=(personal_notes_filter),
            ),
        ).annotate(
            participation_count=Count(
                "filtered_participation_statuses",
                filter=Q(filtered_participation_statuses__absence_reason__isnull=True),
                distinct=True,
            ),
            absence_count=Count(
                "filtered_participation_statuses",
                filter=Q(filtered_participation_statuses__absence_reason__count_as_absent=True),
                distinct=True,
            ),
            tardiness_sum=Sum("filtered_participation_statuses__tardiness", distinct=True),
            tardiness_count=Count(
                "filtered_participation_statuses",
                filter=Q(filtered_participation_statuses__tardiness__gt=0),
                distinct=True,
            ),
        )

    persons = persons.order_by("last_name", "first_name")

    for absence_reason in AbsenceReason.objects.all():
        persons = persons.annotate(
            **{
                absence_reason.count_label: Count(
                    "filtered_participation_statuses",
                    filter=Q(
                        filtered_participation_statuses__absence_reason=absence_reason,
                    ),
                    distinct=True,
                )
            }
        )

    for extra_mark in ExtraMark.objects.all():
        persons = persons.annotate(
            **{
                extra_mark.count_label: Count(
                    "filtered_personal_notes",
                    filter=Q(filtered_personal_notes__extra_mark=extra_mark),
                    distinct=True,
                )
            }
        )

    return persons


def annotate_person_statistics_from_documentations(
    persons: QuerySet[Person], docs: QuerySet[Documentation]
) -> QuerySet[Person]:
    """Annotate a queryset of persons with class register statistics from documentations."""
    docs = list(docs.values_list("pk", flat=True))
    return annotate_person_statistics(
        persons,
        Q(participations__related_documentation__in=docs),
        Q(new_personal_notes__documentation__in=docs),
        ignore_filters=len(docs) == 0,
    )


def annotate_person_statistics_for_school_term(
    persons: QuerySet[Person], school_term: SchoolTerm, group: Group | None = None
) -> QuerySet[Person]:
    """Annotate a queryset of persons with class register statistics for a school term."""
    documentations = Documentation.objects.filter(
        datetime_start__date__gte=school_term.date_start,
        datetime_end__date__lte=school_term.date_end,
    )
    if group:
        documentations = documentations.filter(
            pk__in=Documentation.objects.filter(course__groups=group)
            .values_list("pk", flat=True)
            .union(
                Documentation.objects.filter(course__groups__parent_groups=group).values_list(
                    "pk", flat=True
                )
            )
        )
    return annotate_person_statistics_from_documentations(persons, documentations)
