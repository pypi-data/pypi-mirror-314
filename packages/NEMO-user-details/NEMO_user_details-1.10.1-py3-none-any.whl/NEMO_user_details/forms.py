from django.contrib.auth.models import Group
from django.forms import HiddenInput, ModelMultipleChoiceField, models

from NEMO_user_details.customizations import UserDetailsCustomization
from NEMO_user_details.models import UserDetails


# Base details form for admin. We are setting disabled and required attributes here
class UserDetailsAdminForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        disable_fields, require_fields = UserDetailsCustomization.disable_require_fields()
        for field_name in require_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
        for field_name in disable_fields:
            if field_name in self.fields:
                self.fields[field_name].disabled = True
                self.fields[field_name].required = False
                self.fields[field_name].widget = HiddenInput()

    class Meta:
        model = UserDetails
        exclude = ["user"]


# Details form for users page (groups are already on the admin form for users, but we need to add them explicitly here)
class UserDetailsForm(UserDetailsAdminForm):
    groups = ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
    )

    def save(self, commit=True):
        details: UserDetails = super().save(commit=commit)
        if UserDetailsCustomization.get_bool("user_details_enable_groups"):
            details.user.groups.set(self.cleaned_data["groups"])
        return details
