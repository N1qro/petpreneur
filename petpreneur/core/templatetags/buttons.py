import typing

import django.template


register = django.template.Library()
StateType = typing.Literal["primary", "hovered", "focused"]
ButtonColor = typing.Literal["default", "black", "red"]


@register.inclusion_tag("includes/button.html")
def button(
    text: str,
    state: StateType = "primary",
    color: ButtonColor = "default",
):
    return {
        "tag": "button",
        "text": text,
        "state": state,
        "color": color,
    }


@register.inclusion_tag("includes/button.html")
def link_button(
    text: str,
    href: str = "#",
    state: StateType = "primary",
    color: ButtonColor = "default",
):
    return {
        "tag": "a",
        "text": text,
        "state": state,
        "color": color,
        "href": href,
    }


@register.inclusion_tag("includes/button.html")
def submit_button(
    text: str,
    state: StateType = "hovered",
    color: ButtonColor = "black",
    name: str = "submit",
    value: typing.Union[str, None] = None,
):
    return {
        "tag": "button",
        "type": "submit",
        "text": text,
        "state": state,
        "color": color,
        "name": name,
        "value": value,
    }


__all__ = []
