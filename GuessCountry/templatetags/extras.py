from django.contrib.auth import get_user_model
from django import template
from django.utils.html import format_html

user_model = get_user_model()

register = template.Library()


@register.filter
def user_details(user, current_user):
    if not isinstance(user, user_model):
        # Return empty string as safe default.
        return ''
    
    if user.first_name and user.last_name:
        name = f"{user.first_name} {user.last_name}"
    elif user.first_name:
        name = f"{user.first_name}"
    elif user.last_name:
        name = f"{user.last_name}"
    else:
        name = f"{user.username}"
    
    if user != current_user:
        if user.email:
            prefix = format_html('<a href="mailto:{}">', user.email)
            suffix = format_html("</a>")
        else:
            prefix = ""
            suffix = ""
    else:
        prefix = ""
        suffix = ""
    
    return format_html('{}{}{}', prefix, name, suffix)
