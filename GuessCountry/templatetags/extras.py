from django.contrib.auth import get_user_model
from django import template
from django.utils.html import format_html

from GuessCountry.models import Country

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
def country_details(country, name_visible=True):
    if not isinstance(country, Country):
        return ''
    
    capital = format_html('<p>Capital: {}</p>', country.capital)
    region = format_html('<p>Region: {}</p>', country.region)
    population = format_html('<p>Population: {}</p>', country.population)
    flag = format_html('<p><img src={} class="img-thumbnail"></p>', country.flag)
    
    if name_visible:
        name = format_html('<h2>{}</h2>', country.name)
        formatted_date = country.modified_at.strftime("%d-%b-%y")
        last_updated = format_html('<p>Last updated: {}</p>', formatted_date)
        
        return format_html('{}{}{}{}{}{}',
                           name, capital, region,
                           population, flag, last_updated)
    else:
        name = format_html(
            '''
            <details>
                <summary>Mystery country</summary>
                <h2>{}</h2>
            </details>
            ''',
            country.name)
        return format_html('{}{}{}{}{}',
                           capital, region, population,
                           flag, name)


@register.filter
def hours_to_sec(value):
    return value * 60 * 60
