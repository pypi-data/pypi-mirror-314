from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from material import Layout, Row

from aleksis.core.models import Group, Person
from aleksis.core.util.core_helpers import get_site_preferences

from .models import (
    GroupRole,
    GroupRoleAssignment,
)


class GroupRoleForm(forms.ModelForm):
    layout = Layout("name", "icon", "colour")

    class Meta:
        model = GroupRole
        fields = ["name", "icon", "colour"]


class AssignGroupRoleForm(forms.ModelForm):
    layout_base = ["groups", "person", "role", Row("date_start", "date_end")]

    groups = forms.ModelMultipleChoiceField(
        label=_("Group"),
        required=True,
        queryset=Group.objects.all(),
        widget=ModelSelect2MultipleWidget(
            model=Group,
            search_fields=["name__icontains", "short_name__icontains"],
            attrs={
                "data-minimum-input-length": 0,
                "class": "browser-default",
            },
        ),
    )
    person = forms.ModelChoiceField(
        label=_("Person"),
        required=True,
        queryset=Person.objects.all(),
        widget=ModelSelect2Widget(
            model=Person,
            search_fields=[
                "first_name__icontains",
                "last_name__icontains",
                "short_name__icontains",
            ],
            attrs={"data-minimum-input-length": 0, "class": "browser-default"},
        ),
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        initial = kwargs.get("initial", {})

        # Build layout with or without groups field
        base_layout = self.layout_base[:]
        if "groups" in initial:
            base_layout.remove("groups")
        self.layout = Layout(*base_layout)

        super().__init__(*args, **kwargs)

        if "groups" in initial:
            self.fields["groups"].required = False

        # Filter persons and groups by permissions
        if not self.request.user.has_perm("alsijil.assign_grouprole"):  # Global permission
            persons = Person.objects
            if initial.get("groups"):
                persons = persons.filter(member_of__in=initial["groups"])
            if get_site_preferences()["alsijil__group_owners_can_assign_roles_to_parents"]:
                persons = persons.filter(
                    Q(member_of__owners=self.request.user.person)
                    | Q(children__member_of__owners=self.request.user.person)
                )
            else:
                persons = persons.filter(member_of__owners=self.request.user.person)
            self.fields["person"].queryset = persons.distinct()

            if "groups" not in initial:
                groups = (
                    Group.objects.for_current_school_term_or_all()
                    .filter(
                        Q(owners=self.request.user.person)
                        | Q(parent_groups__owners=self.request.user.person)
                        if get_site_preferences()["alsijil__inherit_privileges_from_parent_group"]
                        else Q(owners=self.request.user.person)
                    )
                    .distinct()
                )
                self.fields["groups"].queryset = groups

    def clean_groups(self):
        """Ensure that only permitted groups are used."""
        return self.initial["groups"] if "groups" in self.initial else self.cleaned_data["groups"]

    class Meta:
        model = GroupRoleAssignment
        fields = ["groups", "person", "role", "date_start", "date_end"]


class GroupRoleAssignmentEditForm(forms.ModelForm):
    class Meta:
        model = GroupRoleAssignment
        fields = ["date_start", "date_end"]
