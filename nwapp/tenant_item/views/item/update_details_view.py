# -*- coding: utf-8 -*-
from ipware import get_client_ip
import django_filters
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from django.conf.urls import url, include
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import filters
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response

from shared_foundation.drf.permissions import SharedUserIsActivePermission, DisableOptionsPermission, TenantPermission
# from tenant_api.filters.item_type import ItemFilter
# from tenant_api.pagination import TinyResultsSetPagination
# from tenant_api.permissions.item_type import (
#    CanListCreateItemPermission,
#    CanRetrieveItemPermission
# )
from tenant_item.serializers import (
    ItemRetrieveSerializer,
    IncidentDetailsUpdateSerializer,
    EventDetailsUpdateSerializer,
    ConcernDetailsUpdateSerializer,
    InformationDetailsUpdateSerializer,
    CommunityNewsDetailsUpdateSerializer,
    VolunteerDetailsUpdateSerializer,
    ResourceDetailsUpdateSerializer
)
from tenant_foundation.models import Item, ItemType


class ItemDetailsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ItemRetrieveSerializer
    # pagination_class = TinyResultsSetPagination
    permission_classes = (
        DisableOptionsPermission,
        permissions.IsAuthenticated,
        SharedUserIsActivePermission,
        TenantPermission,
        # CanRetrieveItemPermission
    )

    @transaction.atomic
    def put(self, request, slug=None):
        """
        Retrieve
        """
        object = get_object_or_404(Item, slug=slug)
        self.check_object_permissions(request, object)  # Validate permissions.
        serializer = None
        type_of = object.type_of.category

        if type_of == ItemType.CATEGORY.INCIDENT:
            write_serializer = IncidentDetailsUpdateSerializer(
                object,
                data=request.data,
                context={
                    'request': request,
                    'type_of': object.type_of.category,
                }
            )
            write_serializer.is_valid(raise_exception=True)
            object = write_serializer.save()

        elif type_of == ItemType.CATEGORY.EVENT:
            write_serializer = EventDetailsUpdateSerializer(
                object,
                data=request.data,
                context={
                    'request': request,
                    'type_of': object.type_of.category,
                }
            )
            write_serializer.is_valid(raise_exception=True)
            object = write_serializer.save()

        elif type_of == ItemType.CATEGORY.CONCERN:
            write_serializer = ConcernDetailsUpdateSerializer(
                object,
                data=request.data,
                context={
                    'request': request,
                    'type_of': object.type_of.category,
                }
            )
            write_serializer.is_valid(raise_exception=True)
            object = write_serializer.save()

        elif type_of == ItemType.CATEGORY.INFORMATION:
            write_serializer = InformationDetailsUpdateSerializer(
                object,
                data=request.data,
                context={
                    'request': request,
                    'type_of': object.type_of.category,
                }
            )
            write_serializer.is_valid(raise_exception=True)
            object = write_serializer.save()

        elif type_of == ItemType.CATEGORY.COMMUNITY_NEWS:
            write_serializer = CommunityNewsDetailsUpdateSerializer(
                object,
                data=request.data,
                context={
                    'request': request,
                    'type_of': object.type_of.category,
                }
            )
            write_serializer.is_valid(raise_exception=True)
            object = write_serializer.save()

        elif type_of == ItemType.CATEGORY.VOLUNTEER:
            write_serializer = VolunteerDetailsUpdateSerializer(
                object,
                data=request.data,
                context={
                    'request': request,
                    'type_of': object.type_of.category,
                }
            )
            write_serializer.is_valid(raise_exception=True)
            object = write_serializer.save()

        elif type_of == ItemType.CATEGORY.RESOURCE:
            write_serializer = ResourceDetailsUpdateSerializer(
                object,
                data=request.data,
                context={
                    'request': request,
                    'type_of': object.type_of.category,
                }
            )
            write_serializer.is_valid(raise_exception=True)
            object = write_serializer.save()

        else:
            return Response(data={}, status=status.HTTP_501_NOT_IMPLEMENTED)


        read_serializer = ItemRetrieveSerializer(
            object,
            many=False,
            context={'request': request,}
        )
        return Response(read_serializer.data, status=status.HTTP_200_OK)
