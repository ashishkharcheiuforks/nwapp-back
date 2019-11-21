# -*- coding: utf-8 -*-
import csv
import pytz
from datetime import date, datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# def get_expiry_date(days=2):
#     """Returns the current date plus paramter number of days."""
#     return timezone.now() + timedelta(days=days)


class TagManager(models.Manager):
    def delete_all(self):
        items = Tag.objects.all()
        for item in items.all():
            item.delete()


@transaction.atomic



class Tag(models.Model):

    '''
    METADATA
    '''

    class Meta:
        app_label = 'tenant_foundation'
        db_table = 'nwapp_tags'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        default_permissions = ()
        permissions = ()

    '''
    OBJECT MANAGERS
    '''

    objects = TagManager()

    '''
    MODEL FIELDS
    '''

    text = models.CharField(
        _("Text"),
        max_length=31,
        help_text=_('The text content of this tag.'),
        db_index=True,
        unique=True
    )
    description = models.TextField(
        _("Description"),
        help_text=_('A short description of this tag.'),
        blank=True,
        null=True,
        default='',
    )
    is_archived = models.BooleanField(
        _("Is Archived"),
        help_text=_('Indicates whether tag was archived.'),
        default=False,
        blank=True,
        db_index=True
    )

    """
    MODEL FUNCTIONS
    """

    def __str__(self):
        return str(self.text)
