# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response

from shared_foundation.drf.permissions import SharedUserIsActivePermission, DisableOptionsPermission, TenantPermission
from tenant_foundation.models import AreaCoordinatorAddress
from tenant_area_coordinator.permissions import CanRetrieveUpdateDestroyAreaCoordinatorNodePermission
from tenant_area_coordinator.serializers import AreaCoordinatorRetrieveSerializer, AreaCoordinatorAddressUpdateSerializer


class AreaCoordinatorAddressUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        DisableOptionsPermission,
        permissions.IsAuthenticated,
        SharedUserIsActivePermission,
        TenantPermission,
        CanRetrieveUpdateDestroyAreaCoordinatorNodePermission
    )

    @transaction.atomic
    def put(self, request, slug=None):
        """
        Update
        """
        object = get_object_or_404(AreaCoordinatorAddress, member__user__slug=slug)
        self.check_object_permissions(request, object)  # Validate permissions.
        write_serializer = AreaCoordinatorAddressUpdateSerializer(
            object,
            data=request.data,
            context={
                'request': request,
            }
        )
        write_serializer.is_valid(raise_exception=True)
        object = write_serializer.save()
        read_serializer = AreaCoordinatorRetrieveSerializer(
            object.member,
            many=False,
            context={
                'request': request,
            }
        )
        return Response(read_serializer.data, status=status.HTTP_200_OK)
