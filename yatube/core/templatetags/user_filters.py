from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def addtype(field, css):
    return field.as_widget(attrs={"type": css})

@register.filter
def addvalue(field, css):
    return field.as_widget(attrs={"value": css})

@register.filter
def addaria_labele(field, css):
    return field.as_widget(attrs={"aria-label": css})

@register.filter
def addreadonly(field):
    return field.as_widget(attrs={"readonly"})