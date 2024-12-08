from graphene_django import DjangoObjectType

from aleksis.apps.alsijil.models import NewPersonalNote
from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
)


class PersonalNoteType(
    OptimisticResponseTypeMixin,
    PermissionsTypeMixin,
    DjangoFilterMixin,
    DjangoObjectType,
):
    class Meta:
        model = NewPersonalNote
        fields = (
            "id",
            "note",
            "extra_mark",
            "documentation",
        )


class PersonalNoteBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = NewPersonalNote
        type_name = "BatchCreatePersonalNoteInput"
        return_field_name = "personalNotes"
        fields = ("note", "extra_mark", "documentation", "person")
        permissions = ("alsijil.edit_personal_note_rule",)


class PersonalNoteBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = NewPersonalNote
        type_name = "BatchPatchPersonalNoteInput"
        return_field_name = "personalNotes"
        fields = ("id", "note", "extra_mark", "documentation", "person")
        permissions = ("alsijil.edit_personal_note_rule",)


class PersonalNoteBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = NewPersonalNote
        permissions = ("alsijil.edit_personal_note_rule",)
