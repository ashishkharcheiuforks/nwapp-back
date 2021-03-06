# -*- coding: utf-8 -*-
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from django.conf.urls import url, include
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import filters
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response

from shared_foundation.drf.permissions import SharedUserIsActivePermission, DisableOptionsPermission, TenantPermission
from tenant_staff.permissions import CanRetrieveUpdateDestroyStaffPermission
from tenant_staff.serializers import StaffAvatarCreateOrUpdateOperationSerializer


class StaffAvatarCreateOrUpdateOperationAPIView(generics.CreateAPIView):
    serializer_class = StaffAvatarCreateOrUpdateOperationSerializer
    permission_classes = (
        DisableOptionsPermission,
        permissions.IsAuthenticated,
        SharedUserIsActivePermission,
        TenantPermission,
        CanRetrieveUpdateDestroyStaffPermission
    )

    @transaction.atomic
    def post(self, request, format=None):
        serializer = StaffAvatarCreateOrUpdateOperationSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
