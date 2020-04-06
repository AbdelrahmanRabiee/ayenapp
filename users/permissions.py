"""permissions for users app."""
from __future__ import unicode_literals

from rest_framework import permissions


class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    """The request is authenticated as a user, or is a post request."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)