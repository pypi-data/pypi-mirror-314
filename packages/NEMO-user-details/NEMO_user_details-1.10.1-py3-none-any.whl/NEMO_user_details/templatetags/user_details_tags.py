from django import template

register = template.Library()


@register.filter
def app_installed(app_name):
    from django.apps import apps

    return apps.is_installed(app_name)
