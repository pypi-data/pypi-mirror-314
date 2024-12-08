from django.core.exceptions import PermissionDenied

import graphene
from graphene_django import bypass_get_queryset
from graphene_django.types import DjangoObjectType
from reversion import create_revision, set_comment, set_user

from aleksis.apps.alsijil.util.predicates import (
    can_edit_documentation,
    is_in_allowed_time_range,
    is_in_allowed_time_range_for_participation_status,
)
from aleksis.apps.alsijil.util.predicates import (
    can_edit_participation_status as can_edit_participation_status_predicate,
)
from aleksis.apps.chronos.schema import LessonEventType
from aleksis.apps.cursus.models import Subject
from aleksis.apps.cursus.schema import CourseType, SubjectType
from aleksis.core.models import Person
from aleksis.core.schema.base import (
    DjangoFilterMixin,
    PermissionsTypeMixin,
)
from aleksis.core.util.core_helpers import has_person

from ..models import Documentation
from .participation_status import ParticipationStatusType


class DocumentationType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Documentation
        fields = (
            "id",
            "course",
            "subject",
            "topic",
            "homework",
            "group_note",
            "datetime_start",
            "datetime_end",
            "date_start",
            "date_end",
            "teachers",
        )
        filter_fields = {
            "id": ["exact", "lte", "gte"],
            "course__name": ["exact"],
        }

    course = graphene.Field(CourseType, required=False)
    amends = graphene.Field(lambda: LessonEventType, required=False)
    subject = graphene.Field(SubjectType, required=False)
    participations = graphene.List(ParticipationStatusType, required=False)

    future_notice = graphene.Boolean(required=False)
    future_notice_participation_status = graphene.Boolean(required=False)

    can_edit_participation_status = graphene.Boolean(required=False)
    can_view_participation_status = graphene.Boolean(required=False)

    old_id = graphene.ID(required=False)

    @staticmethod
    @bypass_get_queryset
    def resolve_amends(root: Documentation, info, **kwargs):
        if hasattr(root, "_amends_prefetched"):
            return root._amends_prefetched
        return root.amends

    @staticmethod
    @bypass_get_queryset
    def resolve_teachers(root: Documentation, info, **kwargs):
        if not str(root.pk).startswith("DUMMY") and hasattr(root, "teachers"):
            return root.teachers
        elif root.amends.amends:
            if root.amends.teachers:
                return root.amends.teachers
            else:
                return root.amends.amends.teachers
        return root.amends.teachers

    @staticmethod
    def resolve_future_notice(root: Documentation, info, **kwargs):
        """Show whether the user can't edit the documentation because it's in the future."""
        return not is_in_allowed_time_range(info.context.user, root) and can_edit_documentation(
            info.context.user, root
        )

    @staticmethod
    def resolve_future_notice_participation_status(root: Documentation, info, **kwargs):
        """Shows whether the user can edit all participation statuses based on the current time.

        This checks whether the documentation is in the future.
        """
        return not is_in_allowed_time_range_for_participation_status(info.context.user, root)

    @staticmethod
    def resolve_can_edit_participation_status(root: Documentation, info, **kwargs):
        """Shows whether the user can edit all participation statuses of the documentation"""
        return can_edit_participation_status_predicate(info.context.user, root)

    @staticmethod
    def resolve_can_view_participation_status(root: Documentation, info, **kwargs):
        """Shows whether the user can view all participation statuses of the documentation"""
        return info.context.user.has_perm(
            "alsijil.view_participation_status_for_documentation_rule", root
        )

    @staticmethod
    @bypass_get_queryset
    def resolve_participations(root: Documentation, info, **kwargs):
        # A dummy documentation will not have any participations
        if str(root.pk).startswith("DUMMY") or not hasattr(root, "participations"):
            return []
        elif not info.context.user.has_perm(
            "alsijil.view_participation_status_for_documentation_rule", root
        ):
            if has_person(info.context.user):
                return [
                    p for p in root.participations.all() if p.person == info.context.user.person
                ]
            return []

        # Annotate participations with prefetched documentation data for personal notes
        for participation in root.participations.all():
            participation._prefetched_documentation = root

        return root.participations.all()


class DocumentationInputType(graphene.InputObjectType):
    id = graphene.ID(required=True)
    course = graphene.ID(required=False)
    subject = graphene.ID(required=False)
    teachers = graphene.List(graphene.ID, required=False)

    topic = graphene.String(required=False)
    homework = graphene.String(required=False)
    group_note = graphene.String(required=False)


class LessonsForPersonType(graphene.ObjectType):
    id = graphene.ID()  # noqa
    lessons = graphene.List(DocumentationType)


class DocumentationBatchCreateOrUpdateMutation(graphene.Mutation):
    class Arguments:
        input = graphene.List(DocumentationInputType)

    documentations = graphene.List(DocumentationType)

    @classmethod
    def create_or_update(cls, info, doc):
        _id = doc.id

        # Sadly, we can't use the update_or_create method since create_defaults
        # is only introduced in Django 5.0
        obj, __ = Documentation.get_or_create_by_id(_id, info.context.user)

        if doc.topic is not None:
            obj.topic = doc.topic
        if doc.homework is not None:
            obj.homework = doc.homework
        if doc.group_note is not None:
            obj.group_note = doc.group_note

        if doc.subject is not None:
            obj.subject = Subject.objects.get(pk=doc.subject)
        if doc.teachers is not None:
            obj.teachers.set(Person.objects.filter(pk__in=doc.teachers))

        obj.save()
        return obj

    @classmethod
    def mutate(cls, root, info, input):  # noqa
        with create_revision():
            set_user(info.context.user)
            set_comment("Updated in coursebook")
            objs = [cls.create_or_update(info, doc) for doc in input]

        return DocumentationBatchCreateOrUpdateMutation(documentations=objs)


class TouchDocumentationMutation(graphene.Mutation):
    class Arguments:
        documentation_id = graphene.ID(required=True)

    documentation = graphene.Field(DocumentationType)

    def mutate(root, info, documentation_id):
        documentation, created = Documentation.get_or_create_by_id(
            documentation_id, info.context.user
        )

        if not info.context.user.has_perm(
            "alsijil.edit_participation_status_for_documentation_with_time_range_rule",
            documentation,
        ):
            raise PermissionDenied()

        if not created:
            documentation.touch()

        return TouchDocumentationMutation(documentation=documentation)
