from django import template

register = template.Library()

@register.filter(name='get_quan')
def get_quan(value, arg):
    try:
        return value[arg]['quan']
    except:
        return ""

@register.filter(name='get')
def get(value, arg):
    try:
        return value[arg]
    except:
        return ""


@register.filter(name='get_hird')
def get_hird(value, arg):
    try:
        return value[arg]['hird']
    except:
        return ""


@register.filter(name='get_nothing_hird')
def get_nothing_hird(value, arg):
    try:
        if value[arg]['hird'] == "":
            return True
        return False
    except:
        return False

@register.filter(name='get_nothing_quan')
def get_nothing_quan(value, arg):
    try:
        if value[arg]['quan'] == "":
            return True
        return False
    except:
        return False