# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response

from shared_foundation.drf.permissions import SharedUserIsActivePermission, DisableOptionsPermission, TenantPermission
from tenant_foundation.models import Staff
from tenant_staff.permissions import CanRetrieveUpdateDestroyStaffPermission
from tenant_staff.serializers import StaffRetrieveSerializer, StaffUpdateSerializer


class StaffRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (
        DisableOptionsPermission,
        permissions.IsAuthenticated,
        SharedUserIsActivePermission,
        TenantPermission,
        CanRetrieveUpdateDestroyStaffPermission
    )

    @transaction.atomic
    def get(self, request, slug=None):
        """
        Retrieve
        """
        order = get_object_or_404(Staff, user__slug=slug)
        self.check_object_permissions(request, order)  # Validate permissions.
        serializer = StaffRetrieveSerializer(order, many=False, context={'request': request,})
        # queryset = serializer.setup_eager_loading(self, queryset)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
