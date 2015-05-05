# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.contrib.redirects.models import Redirect


def create_redirect(sender, instance, raw, **kwargs):

    # Only proceed if not raw and we're dealing with an existing object
    if not raw and instance.pk:

        # Only proceed if the contrib redirects app is installed
        if 'django.contrib.redirects' not in settings.INSTALLED_APPS:
            return

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
