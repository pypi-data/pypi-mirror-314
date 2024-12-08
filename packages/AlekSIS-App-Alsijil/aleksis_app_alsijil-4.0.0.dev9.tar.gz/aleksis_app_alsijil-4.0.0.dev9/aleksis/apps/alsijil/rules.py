from rules import add_perm

from aleksis.core.models import Group
from aleksis.core.util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
    is_current_person,
    is_site_preference_set,
)

from .util.predicates import (
    can_edit_documentation,
    can_edit_participation_status,
    can_edit_personal_note,
    can_register_absence_for_at_least_one_group,
    can_register_absence_for_person,
    can_view_documentation,
    can_view_participation_status,
    can_view_personal_note,
    can_view_statistics_for_person,
    has_person_group_object_perm,
    is_course_group_owner,
    is_course_member,
    is_course_teacher,
    is_group_member,
    is_group_owner,
    is_group_role_assignment_group_owner,
    is_in_allowed_time_range,
    is_in_allowed_time_range_for_participation_status,
    is_lesson_event_group_owner,
    is_lesson_event_teacher,
    is_owner_of_any_group,
    is_parent_group_owner,
    is_person_group_owner,
)

# Register absence
view_register_absence_predicate = has_person & (
    can_register_absence_for_at_least_one_group | has_global_perm("alsijil.register_absence")
)
add_perm("alsijil.view_register_absence_rule", view_register_absence_predicate)

register_absence_predicate = has_person & (
    can_register_absence_for_person
    | has_global_perm("alsijil.register_absence")
    | has_object_perm("core.register_absence_person")
    | has_person_group_object_perm("core.register_absence_group")
)
add_perm("alsijil.register_absence_rule", register_absence_predicate)

# View full register for group
view_full_register_predicate = has_person & (
    is_group_owner
    | (
        is_parent_group_owner
        & is_site_preference_set("alsijil", "inherit_privileges_from_parent_group")
    )
    | has_global_perm("alsijil.view_full_register")
    | has_object_perm("core.view_full_register_group")
)
add_perm("alsijil.view_full_register_rule", view_full_register_predicate)


# View extra mark list
view_extramarks_predicate = has_person & has_global_perm("alsijil.view_extramark")
add_perm("alsijil.view_extramarks_rule", view_extramarks_predicate)

# Fetch all extra marks
fetch_extramarks_predicate = has_person
add_perm("alsijil.fetch_extramarks_rule", fetch_extramarks_predicate)

# Add extra mark
add_extramark_predicate = view_extramarks_predicate & has_global_perm("alsijil.add_extramark")
add_perm("alsijil.add_extramark_rule", add_extramark_predicate)

# Edit extra mark
edit_extramark_predicate = view_extramarks_predicate & has_global_perm("alsijil.change_extramark")
add_perm("alsijil.edit_extramark_rule", edit_extramark_predicate)

# Delete extra mark
delete_extramark_predicate = view_extramarks_predicate & has_global_perm("alsijil.delete_extramark")
add_perm("alsijil.delete_extramark_rule", delete_extramark_predicate)

# View group role list
view_group_roles_predicate = has_person & has_global_perm("alsijil.view_grouprole")
add_perm("alsijil.view_grouproles_rule", view_group_roles_predicate)

# Add group role
add_group_role_predicate = view_group_roles_predicate & has_global_perm("alsijil.add_grouprole")
add_perm("alsijil.add_grouprole_rule", add_group_role_predicate)

# Edit group role
edit_group_role_predicate = view_group_roles_predicate & has_global_perm("alsijil.change_grouprole")
add_perm("alsijil.edit_grouprole_rule", edit_group_role_predicate)

# Delete group role
delete_group_role_predicate = view_group_roles_predicate & has_global_perm(
    "alsijil.delete_grouprole"
)
add_perm("alsijil.delete_grouprole_rule", delete_group_role_predicate)

view_assigned_group_roles_predicate = has_person & (
    is_group_owner
    | (
        is_parent_group_owner
        & is_site_preference_set("alsijil", "inherit_privileges_from_parent_group")
    )
    | has_global_perm("alsijil.assign_grouprole")
    | has_object_perm("core.assign_grouprole")
)
add_perm("alsijil.view_assigned_grouproles_rule", view_assigned_group_roles_predicate)

assign_group_role_person_predicate = has_person & (
    is_person_group_owner | has_global_perm("alsijil.assign_grouprole")
)
add_perm("alsijil.assign_grouprole_to_person_rule", assign_group_role_person_predicate)

assign_group_role_for_multiple_predicate = has_person & (
    is_owner_of_any_group | has_global_perm("alsijil.assign_grouprole")
)
add_perm("alsijil.assign_grouprole_for_multiple_rule", assign_group_role_for_multiple_predicate)

assign_group_role_group_predicate = view_assigned_group_roles_predicate
add_perm("alsijil.assign_grouprole_for_group_rule", assign_group_role_group_predicate)

edit_group_role_assignment_predicate = has_person & (
    has_global_perm("alsijil.assign_grouprole") | is_group_role_assignment_group_owner
)
add_perm("alsijil.edit_grouproleassignment_rule", edit_group_role_assignment_predicate)

stop_group_role_assignment_predicate = edit_group_role_assignment_predicate
add_perm("alsijil.stop_grouproleassignment_rule", stop_group_role_assignment_predicate)

delete_group_role_assignment_predicate = has_person & (
    has_global_perm("alsijil.assign_grouprole") | is_group_role_assignment_group_owner
)
add_perm("alsijil.delete_grouproleassignment_rule", delete_group_role_assignment_predicate)

view_register_objects_list_predicate = has_person & (
    has_any_object("core.view_full_register_group", Group)
    | has_global_perm("alsijil.view_full_register")
)
add_perm("alsijil.view_register_objects_list_rule", view_register_objects_list_predicate)

view_documentation_predicate = has_person & (
    has_global_perm("alsijil.view_documentation") | can_view_documentation
)
add_perm("alsijil.view_documentation_rule", view_documentation_predicate)

view_documentations_for_course_predicate = has_person & (
    has_global_perm("alsijil.view_documentation")
    | is_course_teacher
    | is_course_member
    | is_course_group_owner
)
add_perm("alsijil.view_documentations_for_course_rule", view_documentations_for_course_predicate)

view_documentations_for_group_predicate = has_person & (
    has_global_perm("alsijil.view_documentation")
    | is_group_owner
    | is_group_member
    | is_parent_group_owner
)
add_perm("alsijil.view_documentations_for_group_rule", view_documentations_for_group_predicate)

view_documentations_menu_predicate = has_person
add_perm("alsijil.view_documentations_menu_rule", view_documentations_menu_predicate)

view_documentations_for_teacher_predicate = has_person & (
    has_global_perm("alsijil.view_documentation") | is_current_person
)
add_perm("alsijil.view_documentations_for_teacher_rule", view_documentations_for_teacher_predicate)

add_documentation_for_course_predicate = has_person & (
    has_global_perm("alsijil.add_documentation") | is_course_teacher
)
add_perm("alsijil.add_documentation_for_course_rule", add_documentation_for_course_predicate)

add_documentation_for_lesson_event_predicate = has_person & (
    has_global_perm("alsijil.add_documentation")
    | is_lesson_event_teacher
    | is_lesson_event_group_owner
)
add_perm(
    "alsijil.add_documentation_for_lesson_event_rule", add_documentation_for_lesson_event_predicate
)

edit_documentation_predicate = (
    has_person
    & (has_global_perm("alsijil.change_documentation") | can_edit_documentation)
    & is_in_allowed_time_range
)
add_perm("alsijil.edit_documentation_rule", edit_documentation_predicate)
add_perm("alsijil.delete_documentation_rule", edit_documentation_predicate)

view_participation_status_for_documentation_predicate = has_person & (
    has_global_perm("alsijil.change_participationstatus") | can_view_participation_status
)
add_perm(
    "alsijil.view_participation_status_for_documentation_rule",
    view_participation_status_for_documentation_predicate,
)

edit_participation_status_for_documentation_with_time_range_predicate = (
    has_person
    & (has_global_perm("alsijil.change_participationstatus") | can_edit_participation_status)
    & is_in_allowed_time_range_for_participation_status
)
add_perm(
    "alsijil.edit_participation_status_for_documentation_with_time_range_rule",
    edit_participation_status_for_documentation_with_time_range_predicate,
)

edit_participation_status_for_documentation_predicate = has_person & (
    has_global_perm("alsijil.change_participationstatus") | can_edit_participation_status
)
add_perm(
    "alsijil.edit_participation_status_for_documentation_rule",
    edit_participation_status_for_documentation_predicate,
)

view_personal_note_predicate = has_person & (
    has_global_perm("alsijil.change_newpersonalnote") | can_view_personal_note
)
add_perm(
    "alsijil.view_personal_note_rule",
    view_personal_note_predicate,
)

edit_personal_note_predicate = (
    has_person
    & (has_global_perm("alsijil.change_newpersonalnote") | can_edit_personal_note)
    & is_in_allowed_time_range
)
add_perm(
    "alsijil.edit_personal_note_rule",
    edit_personal_note_predicate,
)

view_group_statistics_predicate = has_person & (
    has_global_perm("alsijil.view_participationstatus") | is_group_owner
)
add_perm(
    "alsijil.view_group_statistics_rule",
    view_group_statistics_predicate,
)

view_person_statistics_predicate = has_person & (
    is_current_person
    | has_global_perm("alsijil.view_participationstatus")
    | can_view_statistics_for_person
)
add_perm(
    "alsijil.view_person_statistics_rule",
    view_person_statistics_predicate,
)

# View parent menu entry
view_menu_predicate = has_person & (view_documentations_menu_predicate | view_extramarks_predicate)
add_perm(
    "alsijil.view_menu_rule",
    view_menu_predicate,
)
