from datetime import datetime

from django.db.models import BooleanField, ExpressionWrapper, Q

import graphene
import graphene_django_optimizer

from aleksis.apps.chronos.models import LessonEvent
from aleksis.apps.cursus.models import Course
from aleksis.apps.cursus.schema import CourseType
from aleksis.apps.kolego.models import AbsenceReason
from aleksis.apps.kolego.schema.absence import AbsenceReasonType
from aleksis.core.models import Group, Person
from aleksis.core.schema.base import FilterOrderList
from aleksis.core.schema.group import GroupType
from aleksis.core.schema.person import PersonType
from aleksis.core.util.core_helpers import (
    filter_active_school_term,
    get_active_school_term,
    get_site_preferences,
    has_person,
)

from ..model_extensions import annotate_person_statistics_for_school_term
from ..models import Documentation, ExtraMark, NewPersonalNote, ParticipationStatus
from .absences import (
    AbsencesForPersonsCreateMutation,
)
from .documentation import (
    DocumentationBatchCreateOrUpdateMutation,
    DocumentationType,
    LessonsForPersonType,
    TouchDocumentationMutation,
)
from .extra_marks import (
    ExtraMarkBatchCreateMutation,
    ExtraMarkBatchDeleteMutation,
    ExtraMarkBatchPatchMutation,
    ExtraMarkType,
)
from .participation_status import (
    ExtendParticipationStatusToAbsenceBatchMutation,
    ParticipationStatusBatchPatchMutation,
    ParticipationStatusType,
)
from .personal_note import (
    PersonalNoteBatchCreateMutation,
    PersonalNoteBatchDeleteMutation,
    PersonalNoteBatchPatchMutation,
    PersonalNoteType,
)
from .statistics import StatisticsByPersonType


class Query(graphene.ObjectType):
    documentations_by_course_id = FilterOrderList(
        DocumentationType, course_id=graphene.ID(required=True)
    )
    documentations_for_coursebook = FilterOrderList(
        DocumentationType,
        own=graphene.Boolean(required=True),
        obj_type=graphene.String(required=False),
        obj_id=graphene.ID(required=False),
        date_start=graphene.Date(required=True),
        date_end=graphene.Date(required=True),
        incomplete=graphene.Boolean(required=False),
        absences_exist=graphene.Boolean(required=False),
    )

    groups_by_person = FilterOrderList(GroupType, person=graphene.ID())
    courses_of_person = FilterOrderList(CourseType, person=graphene.ID())

    absence_creation_persons = graphene.List(PersonType)
    lessons_for_persons = graphene.List(
        LessonsForPersonType,
        persons=graphene.List(graphene.ID, required=True),
        start=graphene.DateTime(required=True),
        end=graphene.DateTime(required=True),
    )

    extra_marks = FilterOrderList(ExtraMarkType)

    coursebook_absence_reasons = FilterOrderList(AbsenceReasonType)

    statistics_by_person = graphene.Field(
        StatisticsByPersonType,
        person=graphene.ID(required=True),
    )
    participations_of_person = graphene.List(
        ParticipationStatusType,
        person=graphene.ID(required=True),
    )
    personal_notes_for_person = graphene.List(
        PersonalNoteType,
        person=graphene.ID(required=True),
    )
    statistics_by_group = graphene.List(
        StatisticsByPersonType,
        group=graphene.ID(required=True),
    )

    def resolve_documentations_by_course_id(root, info, course_id, **kwargs):
        documentations = Documentation.objects.filter(
            pk__in=Documentation.objects.filter(course_id=course_id)
            .values_list("id", flat=True)
            .union(
                Documentation.objects.filter(amends__course_id=course_id).values_list(
                    "id", flat=True
                )
            )
        )
        return graphene_django_optimizer.query(documentations, info)

    def resolve_documentations_for_coursebook(
        root,
        info,
        own,
        date_start,
        date_end,
        obj_type=None,
        obj_id=None,
        incomplete=False,
        absences_exist=False,
        **kwargs,
    ):
        if (
            (
                obj_type == "COURSE"
                and not info.context.user.has_perm(
                    "alsijil.view_documentations_for_course_rule", Course.objects.get(id=obj_id)
                )
            )
            or (
                obj_type == "GROUP"
                and not info.context.user.has_perm(
                    "alsijil.view_documentations_for_group_rule", Group.objects.get(id=obj_id)
                )
            )
            or (
                obj_type == "TEACHER"
                and not info.context.user.has_perm(
                    "alsijil.view_documentations_for_teacher_rule", Person.objects.get(id=obj_id)
                )
            )
        ):
            return []

        # Find all LessonEvents for all Lessons of this Course in this date range
        event_params = {
            "own": own,
        }
        if obj_type is not None and obj_id is not None:
            event_params.update(
                {
                    "type": obj_type,
                    "id": obj_id,
                }
            )

        school_term = get_active_school_term(info.context)
        date_start = date_start if date_start > school_term.date_start else school_term.date_start
        date_end = date_end if date_end < school_term.date_end else school_term.date_end

        events = LessonEvent.get_single_events(
            datetime.combine(date_start, datetime.min.time()),
            datetime.combine(date_end, datetime.max.time()),
            info.context,
            event_params,
            with_reference_object=True,
        )

        # Lookup or create documentations and return them all.
        docs, dummies = Documentation.get_documentations_for_events(
            datetime.combine(date_start, datetime.min.time()),
            datetime.combine(date_end, datetime.max.time()),
            events,
            incomplete,
            absences_exist,
        )
        return docs + dummies

    @staticmethod
    def resolve_groups_by_person(root, info, person=None):
        if person:
            person = Person.objects.get(pk=person)
            if not info.context.user.has_perm("core.view_person_rule", person):
                return []
        elif has_person(info.context.user):
            person = info.context.user.person
        else:
            return []

        school_term = get_active_school_term(info.context)

        return (
            Group.objects.for_school_term(school_term)
            .filter(
                pk__in=Group.objects.filter(members=person)
                .values_list("id", flat=True)
                .union(Group.objects.filter(owners=person).values_list("id", flat=True))
                .union(
                    Group.objects.filter(parent_groups__owners=person).values_list("id", flat=True)
                )
            )
            .annotate(
                is_priority=ExpressionWrapper(
                    Q(group_type=get_site_preferences()["alsijil__group_type_priority_coursebook"]),
                    output_field=BooleanField(),
                )
            )
            .order_by("is_priority")
        )

    @staticmethod
    def resolve_courses_of_person(root, info, person=None):
        if person:
            person = Person.objects.get(pk=person)
            if not info.context.user.has_perm("core.view_person_rule", person):
                return []
        elif has_person(info.context.user):
            person = info.context.user.person
        else:
            return []

        school_term = get_active_school_term(info.context)

        return Course.objects.filter(
            pk__in=(
                Course.objects.filter(teachers=person)
                .values_list("id", flat=True)
                .union(Course.objects.filter(groups__members=person).values_list("id", flat=True))
                .union(Course.objects.filter(groups__owners=person).values_list("id", flat=True))
                .union(
                    Course.objects.filter(groups__parent_groups__owners=person).values_list(
                        "id", flat=True
                    )
                )
            )
        ).filter(groups__in=Group.objects.for_school_term(school_term))

    @staticmethod
    def resolve_absence_creation_persons(root, info, **kwargs):
        if not info.context.user.has_perm("alsijil.register_absence"):
            group_types = get_site_preferences()["alsijil__group_types_register_absence"]
            school_term = get_active_school_term(info.context)
            if group_types:
                return Person.objects.filter(
                    member_of__in=Group.objects.for_school_term(school_term).filter(
                        owners=info.context.user.person, group_type__in=group_types
                    )
                )
            else:
                qs = Person.objects.filter(member_of__owners=info.context.user.person)
                return filter_active_school_term(info.context, qs, "member_of__school_term")
        return Person.objects.all()

    @staticmethod
    def resolve_lessons_for_persons(
        root,
        info,
        persons,
        start,
        end,
        **kwargs,
    ):
        """Resolve all lesson events for each person in timeframe start to end."""
        lessons_for_person = []
        for person in persons:
            docs, dummies = Documentation.get_documentations_for_person(
                person,
                start,
                end,
            )

            lessons_for_person.append(LessonsForPersonType(id=person, lessons=docs + dummies))

        return lessons_for_person

    @staticmethod
    def resolve_extra_marks(root, info, **kwargs):
        if info.context.user.has_perm("alsijil.fetch_extramarks_rule"):
            return ExtraMark.objects.all()
        raise []

    @staticmethod
    def resolve_coursebook_absence_reasons(root, info, **kwargs):
        if not info.context.user.has_perm("kolego.fetch_absencereasons_rule"):
            return []
        return AbsenceReason.objects.filter(tags__short_name="class_register")

    @staticmethod
    def resolve_statistics_by_person(root, info, person):
        person = Person.objects.get(pk=person)
        if not info.context.user.has_perm("alsijil.view_person_statistics_rule", person):
            return None
        school_term = get_active_school_term(info.context)
        return graphene_django_optimizer.query(
            annotate_person_statistics_for_school_term(
                Person.objects.filter(id=person.id), school_term
            ).first(),
            info,
        )

    @staticmethod
    def resolve_participations_of_person(root, info, person):
        person = Person.objects.get(pk=person)
        if not info.context.user.has_perm("alsijil.view_person_statistics_rule", person):
            return []
        school_term = get_active_school_term(info.context)
        return graphene_django_optimizer.query(
            ParticipationStatus.objects.filter(
                person=person,
                absence_reason__isnull=False,
                datetime_start__date__gte=school_term.date_start,
                datetime_end__date__lte=school_term.date_end,
            ).order_by("-related_documentation__datetime_start"),
            info,
        )

    @staticmethod
    def resolve_personal_notes_for_person(root, info, person):
        person = Person.objects.get(pk=person)
        if not info.context.user.has_perm("alsijil.view_person_statistics_rule", person):
            return []
        school_term = get_active_school_term(info.context)
        return graphene_django_optimizer.query(
            NewPersonalNote.objects.filter(
                person=person,
                documentation__in=Documentation.objects.filter(
                    datetime_start__date__gte=school_term.date_start,
                    datetime_end__date__lte=school_term.date_end,
                ),
            ).order_by("-documentation__datetime_start"),
            info,
        )

    @staticmethod
    def resolve_statistics_by_group(root, info, group):
        group = Group.objects.get(pk=group)
        if not info.context.user.has_perm("alsijil.view_group_statistics_rule", group):
            return []
        school_term = get_active_school_term(info.context)

        members = group.members.all()
        return graphene_django_optimizer.query(
            annotate_person_statistics_for_school_term(members, school_term, group=group), info
        )


class Mutation(graphene.ObjectType):
    create_or_update_documentations = DocumentationBatchCreateOrUpdateMutation.Field()
    touch_documentation = TouchDocumentationMutation.Field()
    update_participation_statuses = ParticipationStatusBatchPatchMutation.Field()
    create_absences_for_persons = AbsencesForPersonsCreateMutation.Field()
    extend_participation_statuses = ExtendParticipationStatusToAbsenceBatchMutation.Field()

    create_extra_marks = ExtraMarkBatchCreateMutation.Field()
    update_extra_marks = ExtraMarkBatchPatchMutation.Field()
    delete_extra_marks = ExtraMarkBatchDeleteMutation.Field()

    create_personal_notes = PersonalNoteBatchCreateMutation.Field()
    update_personal_notes = PersonalNoteBatchPatchMutation.Field()
    delete_personal_notes = PersonalNoteBatchDeleteMutation.Field()
