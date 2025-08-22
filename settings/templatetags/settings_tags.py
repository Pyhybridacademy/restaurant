from django import template
from ..models import SiteSettings

register = template.Library()

@register.simple_tag
def get_site_setting(key):
    """Get a specific site setting value"""
    settings = SiteSettings.get_settings()
    return getattr(settings, key, '')

@register.inclusion_tag('settings/business_hours.html')
def show_business_hours():
    """Display business hours"""
    settings = SiteSettings.get_settings()
    return {'hours': settings.business_hours_dict}

@register.inclusion_tag('settings/social_links.html')
def show_social_links():
    """Display social media links"""
    settings = SiteSettings.get_settings()
    return {'settings': settings}
