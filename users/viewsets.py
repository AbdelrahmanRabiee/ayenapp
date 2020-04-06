from rest_framework.viewsets import (
    GenericViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter

from users.models import User
from users import serializers
from users.permissions import IsAuthenticatedOrCreate


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    - create new user
    - List logged in user's info
    - update user info
    """
    serializer_class = serializers.UserAuthSerializer
    permission_classes = [IsAuthenticatedOrCreate]

    def list(self, request, *args, **kwargs):
        """Get logged-in user's info."""
        user = self.request.user
        serializer = serializers.UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=serializers.UpdateUserSerializer, permission_classes=[IsAuthenticated])
    def update_profile(self, request, *args, **kwargs):
        """Update profile for authenticated user."""
        serializer = serializers.UpdateUserSerializer(
            data=request.data, instance=request.user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersInfoViewSet(ReadOnlyModelViewSet):
    """
    List all users info and search by name
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer
    filter_backends = (SearchFilter, )
    search_fields = ['name', ]


class UsersFilesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    List user files and search by name
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserFilesSerializer
    filter_backends = (SearchFilter, )
    search_fields = ['name',]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        files = user.files.all()
        return files