from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions

# from shared_foundation.utils import has_permission


class CanListCreateStaffPermission(permissions.BasePermission):
    message = _('You do not have permission to access this API-endpoint.')

    def has_permission(self, request, view):
        # print("has_permission", request.method)  # For debugging purposes only.

        return True #TODO: IMPLEMENT.

        # # --- LIST ---
        # if "GET" in request.method:
        #     return has_permission('can_get_associates', request.user, request.user.groups.all())
        #
        # # --- CREATE ---
        # if "POST" in request.method:
        #    return has_permission('can_post_associate', request.user, request.user.groups.all())

        return False


class CanRetrieveUpdateDestroyStaffPermission(permissions.BasePermission):
    message = _('You do not have permission to access this API-endpoint.')

    def has_object_permission(self, request, view, obj):
        # print("has_object_permission", request.method)  # For debugging purposes only.

        return True #TODO: IMPLEMENT.

        # # --- RETRIEVE ---
        # if "GET" in request.method:
        #     # OWNERSHIP BASED
        #     if request.user == obj.owner:
        #         return True
        #
        #     # PERMISSION BASED
        #     return has_permission('can_get_associate', request.user, request.user.groups.all())
        #
        # # ---UPDATE ---
        # if "PUT" in request.method:
        #     # OWNERSHIP BASED
        #     if request.user == obj.owner:
        #         return True
        #
        #     # PERMISSION BASED
        #     return has_permission('can_put_associate', request.user, request.user.groups.all())
        #
        # # --- DELETE ---
        # if "DELETE" in request.method:
        #     # PERMISSION BASED
        #     return has_permission('can_delete_associate', request.user, request.user.groups.all())

        return False
