# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response

from shared_foundation.drf.permissions import SharedUserIsActivePermission, DisableOptionsPermission, TenantPermission
from tenant_foundation.models import Member
from tenant_member.permissions import CanRetrieveUpdateDestroyMemberPermission
from tenant_member.serializers import MemberRetrieveSerializer, MemberUpdateSerializer


class MemberRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        DisableOptionsPermission,
        permissions.IsAuthenticated,
        SharedUserIsActivePermission,
        TenantPermission,
        CanRetrieveUpdateDestroyMemberPermission
    )

    @transaction.atomic
    def get(self, request, slug=None):
        """
        Retrieve
        """
        order = get_object_or_404(Member, user__slug=slug)
        self.check_object_permissions(request, order)  # Validate permissions.
        serializer = MemberRetrieveSerializer(order, many=False, context={'request': request,})
        # queryset = serializer.setup_eager_loading(self, queryset)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def put(self, request, slug=None):
        """
        Update
        """
        client_ip, is_routable = get_client_ip(self.request)
        object = get_object_or_404(Member, slug=slug)
        self.check_object_permissions(request, object)  # Validate permissions.
        write_serializer = MemberUpdateSerializer(object, data=request.data, context={'request': request,})
        write_serializer.is_valid(raise_exception=True)
        object = write_serializer.save()
        read_serializer = MemberRetrieveSerializer(object, many=False, context={'request': request,})
        return Response(read_serializer.data, status=status.HTTP_200_OK)
