from NEMO.urls import router, sort_urls
from django.urls import path, re_path

from NEMO_user_details import api
from NEMO_user_details.views import email, users


def replace_api_url(url_to_replace, new_config):
    for reg in router.registry:
        if reg[0] == url_to_replace:
            router.registry.remove(reg)
    router.register(*new_config)


router.register(r"users_details/education_level", api.EducationLevelViewSet)
router.register(r"users_details/ethnicity", api.EthnicityViewSet)
router.register(r"users_details/gender", api.GenderViewSet)
router.register(r"users_details/race", api.RaceViewSet)
router.register(r"users_details/users", api.UserWithDetailsViewSet, basename="users_with_details")
replace_api_url("users", (r"users", api.UserWithDetailsViewSet))
router.registry.sort(key=sort_urls)

urlpatterns = [
    # Override modify user page to add user details fields
    re_path(
        r"^user/(?P<user_id>\d+|new)/",
        users.create_or_modify_user_and_details,
        name="create_or_modify_user_and_details",
    ),
    # Override broadcast email to add new search by groups
    path("email_broadcast/", email.email_broadcast, name="email_broadcast"),
    re_path(
        r"^email_broadcast/(?P<audience>tool|area|account|project|project-pis|user|tool-reservation|group)/$",
        email.email_broadcast,
        name="email_broadcast",
    ),
]
