import importlib
from datetime import timedelta
from functools import wraps
from http import HTTPStatus
from logging import getLogger
from typing import List, Optional
from urllib.parse import urljoin

import requests
from NEMO.decorators import any_staff_required
from NEMO.forms import UserForm
from NEMO.models import Area, AreaAccessRecord, PhysicalAccessLevel, Project, Qualification, Tool, User
from NEMO.utilities import render_combine_responses
from NEMO.views.customization import ApplicationCustomization, UserCustomization
from NEMO.views.users import create_or_modify_user, get_identity_service, readonly_users
from django.apps import apps
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Max
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from NEMO_user_details.forms import UserDetailsForm
from NEMO_user_details.models import get_user_details

users_logger = getLogger(__name__)


# TODO: Remove when NEMO 5.3.0 is released
def replace_function(old_function_name, raise_exception=True):
    try:
        pkg, fun_name = old_function_name.rsplit(".", 1)
        pkg_mod = importlib.import_module(pkg)
        old_function = getattr(pkg_mod, fun_name)
    except:
        old_function = None
        if raise_exception:
            raise
        else:
            users_logger.warning(f"Could not replace function: {old_function_name}", exc_info=True)

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(old_function, *args, **kwargs)

        if old_function:
            setattr(pkg_mod, fun_name, wrapper)
        return wrapper

    return decorator


# This is a little tricky since we don't want to rewrite all the logic (especially identity service stuff).
# On GET, we are using our user details template and inserting it onto the original page
# On POST, we have 3 cases:
#   1. original form and details form have no errors, so we proceed and save our details after the user is saved
#   2. original form has errors, in which case we insert our form into the original page
#   3. original form has no errors but details form does, so we have to re-render without calling the original method
@any_staff_required
@require_http_methods(["GET", "POST"])
def create_or_modify_user_and_details(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except (User.DoesNotExist, ValueError):
        user = None
    user_details = get_user_details(user)

    details_dictionary = get_details_dictionary(user)
    readonly = readonly_users(request)
    if readonly or request.method == "GET":
        details_dictionary["form_details"] = UserDetailsForm(instance=user_details)
        original_response = create_or_modify_user(request, user_id)
        return render_combine_responses(
            request, original_response, "NEMO_user_details/user_details.html", details_dictionary
        )
    elif request.method == "POST":
        form = UserForm(request.POST, instance=user)
        details_form = UserDetailsForm(request.POST, instance=user_details)

        details_dictionary["form_details"] = details_form
        if form.is_valid() and details_form.is_valid():
            original_response = create_or_modify_user(request, user_id)
            if isinstance(original_response, HttpResponseRedirectBase):
                # If it's a redirect, that means everything went ok, we can save the corresponding user details
                details_form.instance.user = User.objects.get(username=form.cleaned_data["username"])
                details_form.save()
                return original_response
            else:
                # There was an error and user was not saved, render original combined with details
                return render_combine_responses(
                    request, original_response, "NEMO_user_details/user_details.html", details_dictionary
                )
        elif not form.is_valid():
            # Original form isn't valid, everything we need is in the original response
            original_response = create_or_modify_user(request, user_id)
            return render_combine_responses(
                request, original_response, "NEMO_user_details/user_details.html", details_dictionary
            )
        else:
            # This case is a bit messy, but it's extremely unlikely to happen
            # Original form is valid, but ours isn't. We cannot proceed with original response.
            # We need to rebuild the original dictionary and send it back.
            dictionary = get_original_dictionary_for_errors(request, user)
            dictionary["form"] = form
            response = render(request, "users/create_or_modify_user.html", dictionary)
            return render_combine_responses(
                request, response, "NEMO_user_details/user_details.html", details_dictionary
            )


def get_details_dictionary(user: Optional[User]):
    return {
        "groups": Group.objects.all(),
        "user_groups": Group.objects.filter(user=user.id) if user else [],
    }


def get_original_dictionary_for_errors(request, user):
    # Original dictionary that would be returned in case of error. See NEMO.users.create_or_modify_user method
    # This is copy-pasted directly from the create_or_modify_user method
    identity_service = get_identity_service()
    # Get access levels and sort by area category
    access_levels = list(PhysicalAccessLevel.objects.all().only("name", "area"))
    access_level_for_sort = list(
        set([ancestor for access in access_levels for ancestor in access.area.get_ancestors(include_self=True)])
    )
    access_level_for_sort.sort(key=lambda x: x.tree_category())
    area_access_levels = Area.objects.filter(id__in=[area.id for area in access_level_for_sort])
    dict_area = {}
    for access in access_levels:
        dict_area.setdefault(access.area.id, []).append(access)

    readonly = readonly_users(request)
    dictionary = {
        "projects": Project.objects.filter(active=True, account__active=True),
        "tools": Tool.objects.filter(visible=True),
        "qualifications": Qualification.objects.filter(user=user),
        "area_access_dict": dict_area,
        "area_access_levels": area_access_levels,
        "one_year_from_now": timezone.localdate() + timedelta(days=365),
        "identity_service_available": identity_service.get("available", False),
        "identity_service_domains": identity_service.get("domains", []),
        "allow_document_upload": UserCustomization.get_bool("user_allow_document_upload"),
        "readonly": readonly,
    }

    last_access = AreaAccessRecord.objects.filter(customer=user).values("area_id").annotate(max_date=Max("start"))
    dictionary["last_access"] = {item["area_id"]: item["max_date"] for item in last_access}

    try:
        # Try to load qualification levels if NEMO_ce is installed
        from NEMO.models import QualificationLevel

        dictionary["qualification_levels"]: QualificationLevel.objects.all()
    except:
        pass

    timeout = identity_service.get("timeout", 3)
    site_title = ApplicationCustomization.get("site_title")
    if dictionary["identity_service_available"]:
        try:
            result = requests.get(urljoin(identity_service["url"], "/areas/"), timeout=timeout)
            if result.status_code == HTTPStatus.OK:
                dictionary["externally_managed_physical_access_levels"] = result.json()
            else:
                dictionary["identity_service_available"] = False
                warning_message = f"The identity service encountered a problem while attempting to return a list of externally managed areas. The administrator has been notified to resolve the problem."
                dictionary["warning"] = warning_message
                warning_message += " The HTTP error was {}: {}".format(result.status_code, result.text)
                users_logger.error(warning_message)
        except Exception as e:
            dictionary["identity_service_available"] = False
            warning_message = f"There was a problem communicating with the identity service. {site_title} is unable to retrieve the list of externally managed areas. The administrator has been notified to resolve the problem."
            dictionary["warning"] = warning_message
            warning_message += " An exception was encountered: " + type(e).__name__ + " - " + str(e)
            users_logger.error(warning_message)
    elif identity_service:
        # display warning if identity service is defined but disabled
        dictionary["warning"] = (
            "The identity service is disabled. You will not be able to modify externally managed physical access levels, reset account passwords, or unlock accounts."
        )

    return dictionary


@replace_function("NEMO.views.history.get_log_entries", raise_exception=False)
def new_get_log_entries(old_function, item, content_type):
    logentries = list(old_function(item, content_type))
    if apps.is_installed("auditlog") and isinstance(item, User):
        from auditlog.models import LogEntry

        user_details = get_user_details(item)
        detail_logentries: List[LogEntry] = LogEntry.objects.filter(
            content_type=ContentType.objects.get_for_model(user_details), object_id=user_details.id
        )
        logentries.extend(detail_logentries)
    return logentries
