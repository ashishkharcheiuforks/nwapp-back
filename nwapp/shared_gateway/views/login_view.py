# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.db import connection # Used for django tenants.
from django.http import Http404
from django.utils import timezone
from oauthlib.common import generate_token
from oauth2_provider.models import Application, AbstractApplication, AbstractAccessToken, AccessToken, RefreshToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins # See: http://www.django-rest-framework.org/api-guide/generic-views/#mixins
from rest_framework import authentication, viewsets, permissions, status, parsers, renderers
from rest_framework.response import Response

from shared_gateway.serializers import SharedLoginSerializer, SharedProfileInfoRetrieveUpdateSerializer
from shared_foundation.drf.permissions import DisableOptionsPermission, PublicPermission


class SharedLoginAPIView(APIView):
    """
    API endpoint used for users to input their email and password to get the
    oAuth 2.0 token which can be used in remote resource servers.
    """
    throttle_classes = ()
    permission_classes = (
        DisableOptionsPermission,
        PublicPermission,
    )

    def post(self, request):
        # Serializer to get our login details.
        serializer = SharedLoginSerializer(data=request.data, context={
            'request': request,
        })
        serializer.is_valid(raise_exception=True)
        authenticated_user = serializer.validated_data['authenticated_user']

        # Authenticate with the public.
        login(self.request, authenticated_user)

        # Get our web application authorization.
        application = Application.objects.filter(name=settings.NWAPP_RESOURCE_SERVER_NAME).first()

        # Generate a temporary "access_token" for the login procedure.
        # Once the token expires, the user will use the "refresh_token" to
        # get a more longer lasting "access_token". This is done for security
        # purposes.
        aware_dt = timezone.now()
        expires_dt = aware_dt + timezone.timedelta(days=1)
        access_token = AccessToken.objects.create(
            application=application,
            user=authenticated_user,
            expires=expires_dt,
            token=generate_token(),
            scope='read,write,introspection'
        )

        refresh_token = RefreshToken.objects.create(
            application = application,
            user = authenticated_user,
            access_token=access_token,
            token=generate_token()
        )

        serializer = SharedProfileInfoRetrieveUpdateSerializer(request.user, many=False, context={
            'request': request,
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        return Response(data = serializer.data, status=status.HTTP_200_OK)
