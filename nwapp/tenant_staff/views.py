# -*- coding: utf-8 -*-
import django_filters
from ipware import get_client_ip
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from django.conf import settings
from django.db.models import Q
from django.db import transaction
from django.http import Http404
from django_filters import rest_framework as filters
from django.conf.urls import url, include
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone
from oauth2_provider.models import Application, AbstractApplication, AbstractAccessToken, AccessToken, RefreshToken
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status,  parsers, renderers
from rest_framework.response import Response

from tenant_staff.serializers import StaffListSerializer
from shared_foundation.models import SharedUser
from tenant_foundation.drf import CanListTenantPermission


# class StaffFilter(filters.FilterSet):
#     def enhanced_type_of_filter(self, name, value):
#         """
#         Filter method used to INCLUDE the "other" option along with the filtered
#         option to filter by. This is important because we want the "Other"
#         option to always be listed regardless of time being filtered.
#         """
#         return self.filter(
#             Q(type_of=Staff.TYPE_OF.NONE)|
#             Q(type_of=value)
#         )
#
#     type_of = filters.NumberFilter(method=enhanced_type_of_filter)
#
#     class Meta:
#         model = Staff
#         fields = ['type_of',]


class StaffListAPIView(generics.ListAPIView):
    authentication_classes= (OAuth2Authentication,)
    serializer_class = StaffListSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = (
        # permissions.IsAuthenticated,
        CanListTenantPermission,
        # CanRetrieveUpdateDestroyInvoicePermission
    )
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = StaffFilter

    def get_queryset(self):
        """
        Get list data.
        """
        queryset = SharedUser.objects.filter(
            tenant=self.request.tenant
        ).order_by('id')
        return queryset