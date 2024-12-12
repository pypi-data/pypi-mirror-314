from NEMO.models import BaseModel, User
from NEMO.views.constants import CHAR_FIELD_MAXIMUM_LENGTH
from django.core.exceptions import ValidationError
from django.db import models


class Ethnicity(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAXIMUM_LENGTH, unique=True, help_text="The name of the ethnicity")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ethnicities"
        ordering = ["name"]


class Race(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAXIMUM_LENGTH, unique=True, help_text="The name of the race")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Gender(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAXIMUM_LENGTH, unique=True, help_text="The name of the gender")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class EducationLevel(BaseModel):
    name = models.CharField(
        max_length=CHAR_FIELD_MAXIMUM_LENGTH, unique=True, help_text="The name of the education level"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class UserDetails(BaseModel):
    user = models.OneToOneField(User, related_name="details", on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, null=True, blank=True, help_text="The user's gender", on_delete=models.SET_NULL)
    race = models.ForeignKey(Race, null=True, blank=True, help_text="The user's race", on_delete=models.SET_NULL)
    ethnicity = models.ForeignKey(
        Ethnicity, null=True, blank=True, help_text="The user's ethnicity", on_delete=models.SET_NULL
    )
    education_level = models.ForeignKey(
        EducationLevel, null=True, blank=True, help_text="The user's education level", on_delete=models.SET_NULL
    )
    emergency_contact = models.CharField(
        max_length=CHAR_FIELD_MAXIMUM_LENGTH, blank=True, help_text="The user's emergency contact information"
    )
    phone_number = models.CharField(max_length=40, blank=True, help_text="The user's phone number")
    employee_id = models.CharField(
        max_length=CHAR_FIELD_MAXIMUM_LENGTH, null=True, blank=True, help_text="The user's internal employee id"
    )
    orcid = models.CharField(
        verbose_name="ORCID", max_length=CHAR_FIELD_MAXIMUM_LENGTH, null=True, blank=True, help_text="The user's ORCID"
    )

    def clean(self):
        if self.employee_id:
            not_unique = UserDetails.objects.filter(employee_id=self.employee_id).exclude(id=self.id)
            if not_unique.exists():
                raise ValidationError({"employee_id": "A user with this Employee id already exists."})
        if self.orcid:
            not_unique = UserDetails.objects.filter(orcid=self.orcid).exclude(id=self.id)
            if not_unique.exists():
                raise ValidationError({"orcid": "A user with this ORCID already exists."})

    def __str__(self):
        return f"{self.user.get_name()}'s details"


def get_user_details(user: User):
    try:
        user_details = user.details
    except (UserDetails.DoesNotExist, AttributeError):
        user_details = UserDetails(user=user)
    return user_details
