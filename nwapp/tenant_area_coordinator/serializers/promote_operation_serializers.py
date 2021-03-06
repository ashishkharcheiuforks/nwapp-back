# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
from dateutil import tz
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q, Prefetch
from django.template.loader import render_to_string  # HTML / TXT
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from shared_foundation.constants import *
from shared_foundation.models import SharedUser, SharedGroup
from tenant_foundation.constants import *
from tenant_foundation.models import (
    Comment,
    Member,
    MemberComment,
    AreaCoordinator,
    Associate,
    Staff
)


logger = logging.getLogger(__name__)


class AreaCoordinatorPromoteOperationSerializer(serializers.Serializer):
    area_coordinator = serializers.SlugField(write_only=True, required=True)
    role_id = serializers.ChoiceField(
        write_only=True,
        required=True,
        choices=(
            (MANAGEMENT_GROUP_ID, _('Management')),
            (FRONTLINE_GROUP_ID, _('Frontline')),
            (ASSOCIATE_GROUP_ID, _('Associate')),
        )
    )
    conflict_of_interest_agreement = serializers.BooleanField(write_only=True, required=True,)
    code_of_conduct_agreement = serializers.BooleanField(write_only=True, required=True,)
    confidentiality_agreement = serializers.BooleanField(write_only=True, required=True,)
    associate_agreement = serializers.BooleanField(write_only=True, required=True,)
    staff_agreement = serializers.BooleanField(write_only=True, required=True,)
    police_check_date = serializers.DateField(write_only=True, required=True,)

    def validate(self, dirty_data):
        """
        Override the validation code to add additional functionionality.
        """
        slug = dirty_data.get('area_coordinator')
        area_coordinator = AreaCoordinator.objects.select_for_update().get(user__slug=slug)
        if area_coordinator.user.role_id != SharedGroup.GROUP_MEMBERSHIP.AREA_COORDINATOR:
            raise serializers.ValidationError(_("You cannot promote because this user is not a area coordinator!"))
        return dirty_data

    def create_associate(self, validated_data):
        slug = validated_data.get('area_coordinator')
        area_coordinator = AreaCoordinator.objects.select_for_update().get(user__slug=slug)
        request = self.context.get('request')
        conflict_of_interest_agreement = validated_data.get('conflict_of_interest_agreement')
        code_of_conduct_agreement = validated_data.get('code_of_conduct_agreement')
        confidentiality_agreement = validated_data.get('confidentiality_agreement')
        associate_agreement = validated_data.get('associate_agreement')
        police_check_date = validated_data.get('police_check_date')

        logger.info("Beginning promotion...")

        # Get the text agreement which will be signed.
        conflict_of_interest_agreement = render_to_string('account/conflict_of_interest_agreement/2019_05_01.txt', {})
        code_of_conduct_agreement = render_to_string('account/code_of_conduct_agreement/2019_05_01.txt', {})
        confidentiality_agreement = render_to_string('account/confidentiality_agreement/2019_05_01.txt', {})
        associate_agreement = render_to_string('account/associate_agreement/2019_05_01.txt', {})

        # Create or update our model.
        associate, created = Associate.objects.update_or_create(
            user=area_coordinator.user,
            defaults={
                'user': area_coordinator.user,
                'has_signed_conflict_of_interest_agreement': True,
                'conflict_of_interest_agreement': conflict_of_interest_agreement,
                'conflict_of_interest_agreement_signed_on': timezone.now(),
                'has_signed_code_of_conduct_agreement': True,
                'code_of_conduct_agreement': code_of_conduct_agreement,
                'code_of_conduct_agreement_signed_on': timezone.now(),
                'has_signed_confidentiality_agreement': True,
                'confidentiality_agreement': confidentiality_agreement,
                'confidentiality_agreement_signed_on': timezone.now(),
                'has_signed_associate_agreement': True,
                'associate_agreement': associate_agreement,
                'associate_agreement_signed_on': timezone.now(),
                'police_check_date': police_check_date,
            }
        )

        # Set the user's role to be a area coordinator after clearing the
        # previous group memberships.
        area_coordinator.user.groups.clear()
        area_coordinator.user.groups.add(SharedGroup.GROUP_MEMBERSHIP.ASSOCIATE)

        # raise serializers.ValidationError({ # Uncomment when not using this code but do not delete!
        #     "error": "Terminating for debugging purposes only."
        # })

        logger.info("Promoted to associate")

        return area_coordinator

    def create_staff(self, validated_data):
        slug = validated_data.get('area_coordinator')
        area_coordinator = AreaCoordinator.objects.select_for_update().get(user__slug=slug)
        request = self.context.get('request')
        role_id = validated_data.get('role_id')
        conflict_of_interest_agreement = validated_data.get('conflict_of_interest_agreement')
        code_of_conduct_agreement = validated_data.get('code_of_conduct_agreement')
        confidentiality_agreement = validated_data.get('confidentiality_agreement')
        staff_agreement = validated_data.get('staff_agreement')
        police_check_date = validated_data.get('police_check_date')

        logger.info("Beginning promotion...")

        # Get the text agreement which will be signed.
        conflict_of_interest_agreement = render_to_string('account/conflict_of_interest_agreement/2019_05_01.txt', {})
        code_of_conduct_agreement = render_to_string('account/code_of_conduct_agreement/2019_05_01.txt', {})
        confidentiality_agreement = render_to_string('account/confidentiality_agreement/2019_05_01.txt', {})
        staff_agreement = render_to_string('account/staff_agreement/2019_05_01.txt', {})

        # Create or update our model.
        staff, created = Staff.objects.update_or_create(
            user=area_coordinator.user,
            defaults={
                'user': area_coordinator.user,
                'has_signed_conflict_of_interest_agreement': True,
                'conflict_of_interest_agreement': conflict_of_interest_agreement,
                'conflict_of_interest_agreement_signed_on': timezone.now(),
                'has_signed_code_of_conduct_agreement': True,
                'code_of_conduct_agreement': code_of_conduct_agreement,
                'code_of_conduct_agreement_signed_on': timezone.now(),
                'has_signed_confidentiality_agreement': True,
                'confidentiality_agreement': confidentiality_agreement,
                'confidentiality_agreement_signed_on': timezone.now(),
                'has_signed_staff_agreement': True,
                'staff_agreement': staff_agreement,
                'staff_agreement_signed_on': timezone.now(),
                'police_check_date': police_check_date,
            }
        )

        # Set the user's role to be a area coordinator after clearing the
        # previous group memberships.
        staff.user.groups.clear()
        staff.user.groups.add(role_id)

        # raise serializers.ValidationError({ # Uncomment when not using this code but do not delete!
        #     "error": "Terminating for debugging purposes only."
        # })

        logger.info("Promoted to staff")

        return area_coordinator

    @transaction.atomic
    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality.
        """
        # raise serializers.ValidationError({ # Uncomment when not using this code but do not delete!
        #     "error": "Terminating for debugging purposes only."
        # })

        # Extract the data we are processing.
        role_id = validated_data.get('role_id')

        # Create the object based on the role assigned.
        if role_id == SharedGroup.GROUP_MEMBERSHIP.ASSOCIATE:
            return self.create_associate(validated_data)
        elif role_id == SharedGroup.GROUP_MEMBERSHIP.MANAGER or role_id == SharedGroup.GROUP_MEMBERSHIP.FRONTLINE_STAFF:
            return self.create_staff(validated_data)
