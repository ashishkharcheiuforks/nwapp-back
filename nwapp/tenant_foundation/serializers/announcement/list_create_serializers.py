# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
from dateutil import tz
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from tenant_foundation.models import Announcement


logger = logging.getLogger(__name__)


class AnnouncementListCreateSerializer(serializers.ModelSerializer):

    text = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=Announcement.objects.all(),
            )
        ],
    )
    slug = serializers.CharField(read_only=True,)
    is_archived = serializers.BooleanField(read_only=True)

    # ------ AUDITING ------ #
    created_at = serializers.DateTimeField(read_only=True, allow_null=False,)
    last_modified_at = serializers.DateTimeField(read_only=True, allow_null=False,)

    class Meta:
        model = Announcement
        fields = (
            'slug',
            'text',
            'is_archived',
            'created_at',
            'last_modified_at'
        )

    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality.
        """
        request = self.context.get("request")
        text = validated_data.get('text')

        # Create the district.
        tag = Announcement.objects.create(
            text=text,
            created_by = request.user,
            created_from = request.client_ip,
            created_from_is_public = request.client_ip_is_routable,
            last_modified_by = request.user,
            last_modified_from = request.client_ip,
            last_modified_from_is_public = request.client_ip_is_routable,
        )

        logger.info("New tag was been created.")

        # print(private_file)
        # print("\n")

        # raise serializers.ValidationError({ # Uncomment when not using this code but do not delete!
        #     "error": "Terminating for debugging purposes only."
        # })

        return tag
