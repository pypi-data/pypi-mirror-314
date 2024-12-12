from copy import deepcopy

from NEMO.models import User
from NEMO.serializers import ModelSerializer, UserSerializer
from NEMO.views.api import ModelViewSet, UserViewSet
from rest_framework.fields import CharField

from NEMO_user_details.customizations import UserDetailsCustomization
from NEMO_user_details.models import EducationLevel, Ethnicity, Gender, Race, UserDetails, get_user_details


class GenderSerializer(ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class GenderViewSet(ModelViewSet):
    filename = "user_details_genders"
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    filterset_fields = {
        "id": ["exact", "in", "isnull"],
        "name": ["exact", "iexact", "in", "contains", "icontains", "isempty"],
    }


class RaceSerializer(ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"


class RaceViewSet(ModelViewSet):
    filename = "user_details_races"
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    filterset_fields = {
        "id": ["exact", "in", "isnull"],
        "name": ["exact", "iexact", "in", "contains", "icontains", "isempty"],
    }


class EthnicitySerializer(ModelSerializer):
    class Meta:
        model = Ethnicity
        fields = "__all__"


class EthnicityViewSet(ModelViewSet):
    filename = "user_details_ethnicities"
    queryset = Ethnicity.objects.all()
    serializer_class = EthnicitySerializer
    filterset_fields = {
        "id": ["exact", "in", "isnull"],
        "name": ["exact", "iexact", "in", "contains", "icontains", "isempty"],
    }


class EducationLevelSerializer(ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = "__all__"


class EducationLevelViewSet(ModelViewSet):
    filename = "user_details_ethnicities"
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer
    filterset_fields = {
        "id": ["exact", "in", "isnull"],
        "name": ["exact", "iexact", "in", "contains", "icontains", "isempty"],
    }


class UserDetailsSerializer(ModelSerializer):
    gender_name = CharField(source="gender.name", default=None, read_only=True)
    race_name = CharField(source="race.name", default=None, read_only=True)
    ethnicity_name = CharField(source="ethnicity.name", default=None, read_only=True)
    education_level_name = CharField(source="education_level.name", default=None, read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        disable_fields, require_fields = UserDetailsCustomization.disable_require_fields()
        for disable_field in disable_fields:
            if disable_field in fields:
                del fields[disable_field]
        for require_field in require_fields:
            fields[require_field].required = True
            fields[require_field].allow_blank = False
        return fields

    class Meta:
        model = UserDetails
        exclude = ("user",)


class UserWithDetailsSerializer(UserSerializer):
    details = UserDetailsSerializer(required=False)

    class Meta(UserSerializer.Meta):
        UserSerializer.Meta.expandable_fields.update(
            {
                "gender": ("NEMO_user_details.api.GenderSerializer", {"source": "details.gender"}),
                "race": ("NEMO_user_details.api.RaceSerializer", {"source": "details.race"}),
                "ethnicity": ("NEMO_user_details.api.EthnicitySerializer", {"source": "details.ethnicity"}),
                "education_level": ("NEMO_user_details.api.EducationLevel", {"source": "details.education_level"}),
            }
        )

    def get_fields(self):
        fields = super().get_fields()
        detail_fields = fields.pop("details", {})
        if detail_fields:
            for key, value in detail_fields.fields.items():
                if key != "id":
                    # reset the source to details
                    value.source = "details." + value.source
                    value.source_attrs = value.source.split(".")
                    fields[key] = value
        return fields

    def validate(self, attrs):
        attributes_data = dict(attrs)
        details_attrs = attributes_data.pop("details", {})
        super().validate(attributes_data)
        user_details = get_user_details(self.instance)
        for details_attr, details_value in details_attrs.items():
            setattr(user_details, details_attr, details_value)
        UserDetailsSerializer().full_clean(user_details, exclude=["user"])
        return attrs

    def update(self, instance, validated_data) -> User:
        data = deepcopy(validated_data)
        details_data = data.pop("details", {})
        user_instance = super().update(instance, data)
        user_details = get_user_details(user_instance)
        UserDetailsSerializer().update(user_details, details_data)
        return user_instance

    def create(self, validated_data) -> User:
        data = deepcopy(validated_data)
        details_data = data.pop("details", {})
        user_instance = super().create(data)
        details_data["user"] = user_instance
        UserDetailsSerializer().create(details_data)
        return user_instance


class UserWithDetailsViewSet(UserViewSet):
    serializer_class = UserWithDetailsSerializer
