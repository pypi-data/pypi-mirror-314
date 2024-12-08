from django.core.exceptions import PermissionDenied

from graphene_django import DjangoObjectType

from aleksis.apps.alsijil.models import ExtraMark
from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
)


class ExtraMarkType(
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
    DjangoFilterMixin,
    DjangoObjectType,
):
    class Meta:
        model = ExtraMark
        fields = ("id", "short_name", "name", "colour_fg", "colour_bg", "show_in_coursebook")


class ExtraMarkBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = ExtraMark
        fields = ("short_name", "name", "colour_fg", "colour_bg", "show_in_coursebook")
        optional_fields = ("name",)

    @classmethod
    def check_permissions(cls, root, info, input):  # noqa
        if info.context.user.has_perm("alsijil.create_extramark_rule"):
            return
        raise PermissionDenied()


class ExtraMarkBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = ExtraMark

    @classmethod
    def check_permissions(cls, root, info, input):  # noqa
        if info.context.user.has_perm("alsijil.delete_extramark_rule"):
            return
        raise PermissionDenied()


class ExtraMarkBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = ExtraMark
        fields = ("id", "short_name", "name", "colour_fg", "colour_bg", "show_in_coursebook")

    @classmethod
    def check_permissions(cls, root, info, input):  # noqa
        if info.context.user.has_perm("alsijil.edit_extramark_rule"):
            return
        raise PermissionDenied()
