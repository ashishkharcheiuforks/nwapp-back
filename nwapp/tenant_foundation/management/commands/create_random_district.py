# -*- coding: utf-8 -*-
from freezegun import freeze_time
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from shared_foundation import constants
from shared_foundation.models import SharedUser, SharedOrganization
from tenant_foundation.models import District


class Command(BaseCommand):
    help = _('Command will generate random districts.')

    def add_arguments(self, parser):
        """
        Run manually in console:
        python manage.py create_random_district "london" 1
        """
        parser.add_argument('schema_name', nargs='+', type=str)
        parser.add_argument('length', nargs='+', type=int)

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public() # Switch to Public.

        # Get the user inputs.
        schema_name = options['schema_name'][0]
        length = options['length'][0]

        try:
            organization = SharedOrganization.objects.get(schema_name=schema_name)
        except SharedOrganization.DoesNotExist:
            raise CommandError(_('Organization does not exist!'))

        # Connection will set it back to our tenant.
        connection.set_schema(organization.schema_name, True) # Switch to Tenant.

        districts = District.seed(length)

        # For debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Successfully seed the following district(s):'))
        )

        for district in districts:
            self.stdout.write(
                self.style.SUCCESS(_('Slug %(slug)s.') %{
                    'slug': district.slug,
                })
            )

        # For debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Note: There are %(count)s districts.') % {
                'count': District.objects.all().count()
            })
        )
