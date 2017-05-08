# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


def create_redirect(sender, instance, raw, **kwargs):

    # Only proceed if not raw, we're dealing with an existing object, and the
    # contrib redirects app is installed.
    if not raw and instance.pk \
            and 'django.contrib.redirects' in settings.INSTALLED_APPS:

        from django.contrib.redirects.models import Redirect

        # Only proceed if an existing object exists
        try:
            existing = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        existing_path = existing.get_absolute_url()
        new_path = instance.get_absolute_url()

        if hasattr(instance, 'site') and existing.site != instance.site:
            new_path = '//{0}{1}'.format(instance.site.domain, new_path)

        if existing_path != new_path:
            try:
                redirect = Redirect.objects.get(site=existing.site,
                                                old_path=existing_path)
            except Redirect.DoesNotExist:
                redirect = Redirect(site=existing.site, old_path=existing_path)
            redirect.new_path = new_path
            redirect.save()
