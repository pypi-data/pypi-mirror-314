from typing import Union

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timezone import localdate, now

from rules import predicate

from aleksis.apps.chronos.models import LessonEvent
from aleksis.apps.cursus.models import Course
from aleksis.core.models import Group, Person
from aleksis.core.util.core_helpers import get_site_preferences
from aleksis.core.util.predicates import check_object_permission

from ..models import Documentation, NewPersonalNote


@predicate
def is_group_owner(user: User, obj: Union[Group, Person]) -> bool:
    """Predicate for group owners of a given group.

    Checks whether the person linked to the user is the owner of the given group.
    If there isn't provided a group, it will return `False`.
    """
    if isinstance(obj, Group) and user.person in obj.owners.all():
        return True

    return False


@predicate
def is_person_group_owner(user: User, obj) -> bool:
    """
    Predicate for group owners of any group.

    Checks whether the person linked to the user is
    the owner of any group of the given person.
    """
    return Group.objects.filter(owners=user.person).exists()


@predicate
def can_register_absence_for_at_least_one_group(user: User, obj) -> bool:
    """Predicate for registering absence for at least one group."""
    group_types = get_site_preferences()["alsijil__group_types_register_absence"]
    qs = Group.objects.filter(owners=user.person)
    if not group_types:
        return qs.exists()
    return qs.filter(group_type__in=group_types).exists()


@predicate
def can_register_absence_for_person(user: User, obj: Person) -> bool:
    """Predicate for registering absence for person."""
    group_types = get_site_preferences()["alsijil__group_types_register_absence"]
    qs = obj.member_of.filter(owners=user.person)
    if not group_types:
        return qs.exists()
    return qs.filter(group_type__in=group_types).exists()


def use_prefetched(obj, attr):
    prefetched_attr = f"{attr}_prefetched"
    if hasattr(obj, prefetched_attr):
        return getattr(obj, prefetched_attr)
    return getattr(obj, attr).all()


def has_person_group_object_perm(perm: str):
    """Predicate builder for permissions on a set of member groups.

    Checks whether a user has a permission on any group of a person.
    """
    name = f"has_person_group_object_perm:{perm}"

    @predicate(name)
    def fn(user: User, obj: Person) -> bool:
        groups = use_prefetched(obj, "member_of")
        return any(check_object_permission(user, perm, group, checker_obj=obj) for group in groups)

    return fn


@predicate
def is_group_member(user: User, obj: Union[Group, Person]) -> bool:
    """Predicate for group membership.

    Checks whether the person linked to the user is a member of the given group.
    If there isn't provided a group, it will return `False`.
    """
    if isinstance(obj, Group) and user.person in obj.members.all():
        return True

    return False


@predicate
def is_parent_group_owner(user: User, obj: Group) -> bool:
    """Predicate which checks whether the user is the owner of any parent group of the group."""
    if hasattr(obj, "parent_groups"):
        for parent_group in use_prefetched(obj, "parent_groups"):
            if user.person in use_prefetched(parent_group, "owners"):
                return True
    return False


@predicate
def is_group_role_assignment_group_owner(user: User, obj: Union[Group, Person]) -> bool:
    """Predicate for group owners of a group role assignment.

    Checks whether the person linked to the user is the owner of the groups
    linked to the given group role assignment.
    If there isn't provided a group role assignment, it will return `False`.
    """
    if obj:
        for group in obj.groups.all():
            if user.person in list(group.owners.all()):
                return True
    return False


@predicate
def is_owner_of_any_group(user: User, obj):
    """Predicate which checks if the person is group owner of any group."""
    return Group.objects.filter(owners=user.person).exists()


@predicate
def is_course_teacher(user: User, obj: Course):
    """Predicate for teachers of a course.

    Checks whether the person linked to the user is a teacher in the course.
    """
    if obj:
        return user.person in obj.teachers.all()
    return False


@predicate
def is_lesson_event_teacher(user: User, obj: LessonEvent):
    """Predicate for teachers of a lesson event.

    Checks whether the person linked to the user is a teacher in the lesson event.
    """
    if obj:
        return user.person in obj.all_teachers
    return False


@predicate
def is_course_member(user: User, obj: Course):
    """Predicate for members of a course.

    Checks whether the person linked to the user is a member in the course.
    """
    if obj:
        for g in obj.groups.all():
            if user.person in g.members.all():
                return True
    return False


@predicate
def is_course_group_owner(user: User, obj: Course):
    """Predicate for group owners of a course.

    Checks whether the person linked to the user is a owner of any group
    (or their respective parent groups) linked to the course.
    """
    if obj:
        for g in obj.groups.all():
            if user.person in g.owners.all():
                return True
            for pg in g.parent_groups.all():
                if user.person in pg.owners.all():
                    return True
    return False


@predicate
def is_lesson_event_member(user: User, obj: LessonEvent):
    """Predicate for members of a lesson event.

    Checks whether the person linked to the user is a member in the lesson event,
    or a members of the course, if the lesson event has one.
    """
    if obj:
        for g in obj.groups.all():
            if user.person in g.members.all():
                return True

    return False


@predicate
def is_lesson_event_group_owner(user: User, obj: LessonEvent):
    """Predicate for group owners of a lesson event.

    Checks whether the person linked to the user is a owner of any group
    (or their respective parent groups) linked to the lesson event,
    or a owner of any group linked to the course, if the lesson event has one.
    """
    if obj:
        for g in obj.groups.all():
            if user.person in g.owners.all():
                return True
            for pg in g.parent_groups.all():
                if user.person in pg.owners.all():
                    return True
    return False


@predicate
def is_documentation_teacher(user: User, obj: Documentation):
    """Predicate for teachers of a documentation.

    Checks whether the person linked to the user is a teacher in the documentation.
    """
    if obj:
        if not str(obj.pk).startswith("DUMMY") and hasattr(obj, "teachers"):
            teachers = obj.teachers
        elif obj.amends.amends:
            teachers = obj.amends.teachers if obj.amends.teachers else obj.amends.amends.teachers
        else:
            teachers = obj.amends.teachers
        return user.person in teachers.all()
    return False


@predicate
def can_view_documentation(user: User, obj: Documentation):
    """Predicate which checks if the user is allowed to view a documentation."""
    if obj:
        if is_documentation_teacher(user, obj):
            return True
        if obj.amends:
            return (
                is_lesson_event_teacher(user, obj.amends)
                | is_lesson_event_member(user, obj.amends)
                | is_lesson_event_group_owner(user, obj.amends)
            )
        if obj.course:
            return is_course_teacher(user, obj.course)
    return False


@predicate
def can_view_any_documentation(user: User):
    """Predicate which checks if the user is allowed to view any documentation."""
    allowed_lesson_events = LessonEvent.objects.related_to_person(user.person)

    if allowed_lesson_events.exists():
        return True

    if Documentation.objects.filter(
        Q(teachers=user.person)
        | Q(amends__in=allowed_lesson_events)
        | Q(course__teachers=user.person)
    ).exists():
        return True

    return False


@predicate
def can_edit_documentation(user: User, obj: Documentation):
    """Predicate which checks if the user is allowed to edit or delete a documentation."""
    if obj:
        if is_documentation_teacher(user, obj):
            return True
        if obj.amends:
            return is_lesson_event_teacher(user, obj.amends) | is_lesson_event_group_owner(
                user, obj.amends
            )
    return False


@predicate
def can_view_participation_status(user: User, obj: Documentation):
    """Predicate which checks if the user is allowed to view participation for a documentation."""
    if obj:
        if obj.amends and obj.amends.cancelled:
            return False
        if is_documentation_teacher(user, obj):
            return True
        if obj.amends:
            return is_lesson_event_teacher(user, obj.amends) | is_lesson_event_group_owner(
                user, obj.amends
            )
        if obj.course:
            return is_course_teacher(user, obj.course)
    return False


@predicate
def can_edit_participation_status(user: User, obj: Documentation):
    """Predicate which checks if the user is allowed to edit participation for a documentation."""
    if obj:
        if obj.amends and obj.amends.cancelled:
            return False
        if is_documentation_teacher(user, obj):
            return True
        if obj.amends:
            return is_lesson_event_teacher(user, obj.amends) | is_lesson_event_group_owner(
                user, obj.amends
            )
    return False


@predicate
def is_in_allowed_time_range(user: User, obj: Union[Documentation, NewPersonalNote]):
    """Predicate for documentations or new personal notes with linked documentation.

    Predicate which checks if the given documentation or the documentation linked
    to the given NewPersonalNote is in the allowed time range for editing.
    """
    if isinstance(obj, NewPersonalNote):
        obj = obj.documentation
    if obj and (
        get_site_preferences()["alsijil__allow_edit_future_documentations"] == "all"
        or (
            get_site_preferences()["alsijil__allow_edit_future_documentations"] == "current_day"
            and obj.value_start_datetime(obj).date() <= localdate()
        )
        or (
            get_site_preferences()["alsijil__allow_edit_future_documentations"] == "current_time"
            and obj.value_start_datetime(obj) <= now()
        )
    ):
        return True
    return False


@predicate
def is_in_allowed_time_range_for_participation_status(user: User, obj: Documentation):
    """Predicate which checks if the documentation is in the allowed time range for editing."""
    if obj and obj.value_start_datetime(obj) <= now():
        return True
    return False


@predicate
def can_view_personal_note(user: User, obj: NewPersonalNote):
    """Predicate which checks if the user is allowed to view a personal note."""
    if obj.documentation:
        if is_documentation_teacher(user, obj.documentation):
            return True
        if obj.documentation.amends:
            return is_lesson_event_teacher(
                user, obj.documentation.amends
            ) | is_lesson_event_group_owner(user, obj.documentation.amends)
        if obj.documentation.course:
            return is_course_teacher(user, obj.documentation.course)
    return False


@predicate
def can_edit_personal_note(user: User, obj: NewPersonalNote):
    """Predicate which checks if the user is allowed to edit a personal note."""
    if obj.documentation:
        if is_documentation_teacher(user, obj.documentation):
            return True
        if obj.documentation.amends:
            return is_lesson_event_teacher(
                user, obj.documentation.amends
            ) | is_lesson_event_group_owner(user, obj.documentation.amends)
    return False


@predicate
def can_view_statistics_for_person(user: User, obj: Person) -> bool:
    """Predicate for registering absence for person."""
    group_types = get_site_preferences()["alsijil__group_types_view_person_statistics"]
    qs = obj.member_of.filter(owners=user.person)
    if not group_types.exists():
        return False
    return qs.filter(group_type__in=group_types).exists()
