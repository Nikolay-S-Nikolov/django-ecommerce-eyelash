from django import template

register = template.Library()


@register.inclusion_tag("partials/form_field_error.html")
def render_field_errors(field):
    return {
        "field": field,
    }