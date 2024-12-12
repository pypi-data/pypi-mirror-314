from NEMO.decorators import any_staff_required, replace_function
from NEMO.models import User
from NEMO.typing import QuerySetType
from NEMO.utilities import render_combine_responses
from NEMO.views import email as email_views
from django.contrib.auth.models import Group
from django.views.decorators.http import require_GET

from NEMO_user_details.customizations import UserDetailsCustomization


@any_staff_required
@require_GET
def email_broadcast(request, audience=""):
    original_response = email_views.email_broadcast(request, audience)

    if not UserDetailsCustomization.get_bool("user_details_enable_groups"):
        return original_response

    email_broadcast_dictionary = {}

    if audience == "group":
        email_broadcast_dictionary["group_types"] = Group.objects.all()

    return render_combine_responses(
        request,
        original_response,
        "NEMO_user_details/email_broadcast.html",
        email_broadcast_dictionary,
    )


@replace_function("NEMO.views.email.get_users_for_email")
def new_get_users_for_email(old_function, audience: str, selection, no_type: bool) -> (QuerySetType[User], str):
    if audience != "group":
        return old_function(audience, selection, no_type)
    else:
        user_group_list = User.objects.none()
        for and_group in selection:
            user_group = User.objects.all()
            for group_pk in and_group.split(" "):
                user_group &= User.objects.filter(groups__in=[int(group_pk)])

            user_group_list |= user_group

        return user_group_list.distinct(), None
