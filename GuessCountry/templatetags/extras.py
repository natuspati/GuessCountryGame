from django.contrib.auth import get_user_model
from django import template
from django.utils.html import format_html
from django.conf import settings

from GuessCountry.models import Country
from GuessCountry.api.serializers import CountrySerializer

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


@register.simple_tag
def row(extra_classes=''):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")


@register.filter
def country_details(country, visibility_level=0):
    # If country is given as Country instance, return full information on the model instance.
    if isinstance(country, Country):
        country_dict = CountrySerializer(country).data
        formatted_details = format_item_list(tuple(country_dict.keys()), country_dict)
    
    # If country is given as a dictionary, return format according to visibility level
    elif isinstance(country, dict):
        order_of_country_details = ('population',
                                    'region',
                                    'capital',
                                    'flag',
                                    'name')
        if visibility_level != 0:
            try:
                keys_tuple = order_of_country_details[:-visibility_level]
            except IndexError:
                keys_tuple = order_of_country_details
        else:
            keys_tuple = order_of_country_details
        
        formatted_details = format_item_list(keys_tuple, country)
    
    else:
        formatted_details = ''
    
    return formatted_details


@register.simple_tag(takes_context=True, name='alert_format')
def adopt_result_to_alert(context):
    result = context['result']
    country_name = context['country_name']
    remaining_tries = context['remaining_tries']
    
    if result == 'success':
        alert_class = 'success'
        result_type_message = 'Correct!'
        country_name_message = format_html('Answer is <strong>{}</strong>', country_name)
        # 'Answer is <strong>{}</strong>'.format(country_name)
    elif result == 'wait':
        alert_class = 'info'
        result_type_message = 'Incorrect!'
        country_name_message = format_html('Answer is not <strong>{}</strong>', country_name)
    elif result == 'skip':
        alert_class = 'dark'
        result_type_message = 'Not found!'
        country_name_message = format_html("<strong>{}</strong> doesn't exist", country_name)
    elif result == 'repeat':
        alert_class = 'secondary'
        result_type_message = 'Incorrect!'
        country_name_message = format_html("<strong>{}</strong> already tried", country_name)
    elif result == 'fail':
        alert_class = 'danger'
        result_type_message = 'Out of tries!'
        country_name_message = format_html('Answer is <strong>{}</strong>', country_name)
    else:
        alert_class = 'primary'
        result_type_message = 'Result type'
        country_name_message = 'Country name'
    
    # Last try
    if remaining_tries == 1 and result == 'wait':
        alert_class = 'warning'
        tries_message = format_html('<strong>Last try</strong>', remaining_tries)
    elif remaining_tries < 1:
        tries_message = ''
    else:
        tries_message = format_html('Remaining tries: <strong>{}</strong>.', remaining_tries)
    
    alert_div = format_html(
        '''
        <div class="alert alert-{} alert-dismissible fade show" role="alert">
            <strong>{}</strong> {}. {}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        ''',
        alert_class,
        result_type_message,
        country_name_message,
        tries_message
    )
    
    return alert_div


@register.filter
def hours_to_sec(value):
    return value * 60 * 60


def format_item_list(keys: tuple, country: dict, bootstrap_class='list-group-item'):
    """
    Create bootstrap list-group element using a tuple of country dictionary keys.
    
    :param keys: Tuple of keys that country dictionary must have and will be displayed in the list.
    :param country: Country dictionary deserialized using DRG ModelSerializer.
    :param bootstrap_class: Type of bootstrap item class.
    :return: Unordered list-group safe html element.
    """
    item_tag = ''
    for key in keys:
        if key == 'flag':
            item_tag = format_html(
                '{}<li class="{}"><img src={} class="img-thumbnail"></li>',
                item_tag,
                bootstrap_class,
                country[key]
            )
        else:
            item_tag = format_html(
                '{}<li class="{}">{}: {}</li>',
                item_tag,
                bootstrap_class,
                key.capitalize(),
                country[key]
            )
    
    return format_html('<ul class="list-group">{}</ul>', item_tag)
