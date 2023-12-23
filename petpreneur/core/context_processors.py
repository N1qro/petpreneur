import urllib.parse

import django.conf
import django.core.cache


def mailto_processor(request):
    cache_key = "mailto_link"
    link = django.core.cache.cache.get(cache_key)

    if not link:
        email = django.conf.settings.MAILTO_EMAIL
        subject = django.conf.settings.MAILTO_SUBJECT
        body = django.conf.settings.MAILTO_BODY

        encoded_subject = urllib.parse.quote(subject, safe="")
        encoded_body = urllib.parse.quote(body, safe="")

        link = f"mailto:{email}?subject={encoded_subject}&body={encoded_body}"
        django.core.cache.cache.set(cache_key, link)

    return {cache_key: link}


__all__ = []
