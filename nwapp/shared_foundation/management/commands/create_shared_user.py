# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string  # HTML / TXT
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from shared_foundation.models import SharedUser, SharedGroup


class Command(BaseCommand):
    help = _('Command will create an admin account.')

    def add_arguments(self, parser):
        """
        Run manually in console:
        python manage.py create_shared_user "bart@mikasoftware.com" "123password" "Bart" "Mika";
        """
        parser.add_argument('email', nargs='+', type=str)
        parser.add_argument('password', nargs='+', type=str)
        parser.add_argument('first_name', nargs='+', type=str)
        parser.add_argument('last_name', nargs='+', type=str)

    def handle(self, *args, **options):
        # Get the user inputs.
        email = options['email'][0]
        password = options['password'][0]
        first_name = options['first_name'][0]
        last_name = options['last_name'][0]
        group_id = SharedGroup.GROUP_MEMBERSHIP.EXECUTIVE
        tenant_id = 1 # Public tenant.

        # Defensive Code: Prevent continuing if the email already exists.
        if SharedUser.objects.filter(email=email).exists():
            raise CommandError(_('Email already exists, please pick another email.'))

        # Open up the current "terms of agreement" file and extract the text
        # context which we will save with the user account.
        tos_agreement = render_to_string('account/terms_of_service/2019_05_01.txt', {})

        # Create the user.
        user = SharedUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
            is_superuser=True,
            is_staff=True,
            was_email_activated=True,
            was_onboarded=True,
            has_signed_tos = True,
            tos_agreement = tos_agreement,
            tos_signed_on = timezone.now(),
            tenant_id=tenant_id,
        )

        # Generate and assign the password.
        user.set_password(password)
        user.save()

        # Attach the user to a specific group.
        user.groups.add(group_id)

        # For debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Successfully created an admin account.'))
        )
