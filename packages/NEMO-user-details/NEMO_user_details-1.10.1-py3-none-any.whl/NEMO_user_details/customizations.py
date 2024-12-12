from typing import Set

from NEMO.decorators import customization
from NEMO.views.customization import CustomizationBase


@customization(title="User details", key="user_details")
class UserDetailsCustomization(CustomizationBase):
    variables = {
        "user_details_enable_groups": "",
        "user_details_enable_emergency_contact": "",
        "user_details_enable_phone_number": "",
        "user_details_enable_race": "",
        "user_details_enable_gender": "",
        "user_details_enable_ethnicity": "",
        "user_details_enable_education_level": "",
        "user_details_enable_employee_id": "",
        "user_details_enable_orcid": "",
        "user_details_require_groups": "",
        "user_details_require_emergency_contact": "",
        "user_details_require_phone_number": "",
        "user_details_require_race": "",
        "user_details_require_gender": "",
        "user_details_require_ethnicity": "",
        "user_details_require_education_level": "",
        "user_details_require_employee_id": "",
        "user_details_require_orcid": "",
    }

    @classmethod
    def disable_require_fields(cls) -> (Set[str], Set[str]):
        # This function returns 2 lists:
        # - the first one containing fields to disable
        # - the second one containing fields to require
        # Here we rely on the order of variables where require field option is set after enable
        disable_fields, require_fields = set(), set()
        for var in cls.variables:
            if var.startswith("user_details_enable_"):
                enable_field_name = var.replace("user_details_enable_", "")
                if not cls.get_bool(var):
                    disable_fields.add(enable_field_name)
            elif var.startswith("user_details_require_"):
                require_field_name = var.replace("user_details_require_", "")
                if cls.get_bool(var):
                    require_fields.add(require_field_name)
                    if require_field_name in disable_fields:
                        disable_fields.remove(require_field_name)
        return disable_fields, require_fields
