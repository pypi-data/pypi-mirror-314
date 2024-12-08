from datetime import date, datetime
from typing import TYPE_CHECKING, Optional, Sequence, Union

from django.db.models import QuerySet
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q

from calendarweek import CalendarWeek

from aleksis.core.managers import (
    AlekSISBaseManagerWithoutMigrations,
    RecurrencePolymorphicManager,
)

if TYPE_CHECKING:
    from aleksis.core.models import Group


class GroupRoleManager(AlekSISBaseManagerWithoutMigrations):
    pass


class GroupRoleQuerySet(QuerySet):
    def with_assignments(
        self, time_ref: Union[date, CalendarWeek], groups: Sequence["Group"]
    ) -> QuerySet:
        from aleksis.apps.alsijil.models import GroupRoleAssignment

        if isinstance(time_ref, CalendarWeek):
            qs = GroupRoleAssignment.objects.in_week(time_ref)
        else:
            qs = GroupRoleAssignment.objects.on_day(time_ref)

        qs = qs.for_groups(groups).distinct()
        return self.prefetch_related(
            Prefetch(
                "assignments",
                queryset=qs,
            )
        )


class GroupRoleAssignmentManager(AlekSISBaseManagerWithoutMigrations):
    pass


class GroupRoleAssignmentQuerySet(QuerySet):
    def within_dates(self, start: date, end: date):
        """Filter for all role assignments within a date range."""
        return self.filter(
            Q(date_start__lte=end) & (Q(date_end__gte=start) | Q(date_end__isnull=True))
        )

    def at_time(self, when: Optional[datetime] = None):
        """Filter for role assignments assigned at a certain point in time."""
        now = when or datetime.now()

        return self.on_day(now.date())

    def for_groups(self, groups: Sequence["Group"]):
        """Filter all role assignments for a sequence of groups."""
        qs = self
        for group in groups:
            qs = qs.for_group(group)
        return qs

    def for_group(self, group: "Group"):
        """Filter all role assignments for a group."""
        return self.filter(Q(groups=group) | Q(groups__child_groups=group))


class DocumentationManager(RecurrencePolymorphicManager):
    """Manager adding specific methods to documentations."""


class ParticipationStatusManager(RecurrencePolymorphicManager):
    """Manager adding specific methods to participation statuses."""

    pass
