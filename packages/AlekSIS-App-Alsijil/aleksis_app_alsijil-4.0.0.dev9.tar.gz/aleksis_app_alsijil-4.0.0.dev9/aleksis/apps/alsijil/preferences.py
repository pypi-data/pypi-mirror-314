from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import (
    BooleanPreference,
    ChoicePreference,
    ModelChoicePreference,
    ModelMultipleChoicePreference,
)

from aleksis.core.models import GroupType
from aleksis.core.registries import site_preferences_registry

alsijil = Section("alsijil", verbose_name=_("Class register"))


@site_preferences_registry.register
class InheritPrivilegesFromParentGroup(BooleanPreference):
    section = alsijil
    name = "inherit_privileges_from_parent_group"
    default = True
    verbose_name = _(
        "Grant the owner of a parent group the same privileges "
        "as the owners of the respective child groups "
        "in regard to group role management and generating "
        "full printouts of class registers."
    )


@site_preferences_registry.register
class GroupOwnersCanAssignRolesToParents(BooleanPreference):
    section = alsijil
    name = "group_owners_can_assign_roles_to_parents"
    default = False
    verbose_name = _(
        "Allow group owners to assign group roles to the parents of the group's members"
    )


@site_preferences_registry.register
class AllowEditFutureDocumentations(ChoicePreference):
    """Time range for which documentations may be edited."""

    section = alsijil
    name = "allow_edit_future_documentations"
    default = "current_day"
    choices = (
        ("all", _("Allow editing of all future documentations")),
        (
            "current_day",
            _("Allow editing of all documentations up to and including those on the current day"),
        ),
        (
            "current_time",
            _(
                "Allow editing of all documentations up to and "
                "including those on the current date and time"
            ),
        ),
    )
    verbose_name = _("Set time range for which documentations may be edited")


@site_preferences_registry.register
class GroupTypesRegisterAbsence(ModelMultipleChoicePreference):
    section = alsijil
    name = "group_types_register_absence"
    required = False
    default = []
    model = GroupType
    verbose_name = _(
        "User is allowed to register absences for members "
        "of groups the user is an owner of with these group types"
    )
    help_text = _(
        "If you leave it empty, all member of groups the user is an owner of will be shown."
    )


@site_preferences_registry.register
class GroupTypesViewPersonStatistics(ModelMultipleChoicePreference):
    section = alsijil
    name = "group_types_view_person_statistics"
    required = False
    default = []
    model = GroupType
    verbose_name = _(
        "User is allowed to view coursebook statistics for members "
        "of groups the user is an owner of with these group types"
    )


@site_preferences_registry.register
class GroupTypePriorityCoursebook(ModelChoicePreference):
    section = alsijil
    name = "group_type_priority_coursebook"
    required = False
    default = None
    model = GroupType
    verbose_name = _(
        "Group type of groups to be shown first in the group "
        "select field on the coursebook overview page"
    )
    help_text = _("If you leave it empty, no group type will be used.")

    def get_queryset(self):
        return GroupType.objects.managed_and_unmanaged()
