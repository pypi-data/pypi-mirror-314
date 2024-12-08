import graphene

from aleksis.apps.kolego.models.absence import AbsenceReason
from aleksis.apps.kolego.schema.absence import AbsenceReasonType
from aleksis.core.models import Person
from aleksis.core.schema.person import PersonType

from ..models import ExtraMark
from .extra_marks import ExtraMarkType


class AbsenceReasonWithCountType(graphene.ObjectType):
    absence_reason = graphene.Field(AbsenceReasonType)
    count = graphene.Int()

    def resolve_absence_reason(root, info):
        return root["absence_reason"]

    def resolve_count(root, info):
        return root["count"]


class ExtraMarkWithCountType(graphene.ObjectType):
    extra_mark = graphene.Field(ExtraMarkType)
    count = graphene.Int()

    def resolve_extra_mark(root, info):
        return root["extra_mark"]

    def resolve_count(root, info):
        return root["count"]


class StatisticsByPersonType(graphene.ObjectType):
    person = graphene.Field(PersonType)
    participation_count = graphene.Int()
    absence_count = graphene.Int()
    absence_reasons = graphene.List(AbsenceReasonWithCountType)
    tardiness_sum = graphene.Int()
    tardiness_count = graphene.Int()
    extra_marks = graphene.List(ExtraMarkWithCountType)

    @staticmethod
    def resolve_person(root: Person, info):
        return root

    def resolve_absence_reasons(root, info):
        return [
            dict(absence_reason=reason, count=getattr(root, reason.count_label))
            for reason in AbsenceReason.objects.filter(tags__short_name="class_register")
        ]

    def resolve_tardiness_sum(root, info):
        return root.tardiness_sum

    def resolve_tardiness_count(root, info):
        return root.tardiness_count

    def resolve_extra_marks(root, info):
        return [
            dict(extra_mark=extra_mark, count=getattr(root, extra_mark.count_label))
            for extra_mark in ExtraMark.objects.all()
        ]
