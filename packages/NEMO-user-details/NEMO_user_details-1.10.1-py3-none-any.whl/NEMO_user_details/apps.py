from django.apps import AppConfig


class NEMOUserDetailsConfig(AppConfig):
    name = "NEMO_user_details"
    verbose_name = "NEMO User details"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        # Add group as a valid audience
        from NEMO.forms import EmailBroadcastForm

        EmailBroadcastForm.base_fields["audience"].choices.append(("group", "group"))
