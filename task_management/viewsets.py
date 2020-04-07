
from rest_framework.viewsets import (
    GenericViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django_fsm import can_proceed

from users.models import User
from task_management import serializers


class TasksViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet):
    """
    List user Tasks
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.can_edit:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)    

    def get_queryset(self):
        user = self.request.user
        tasks = user.tasks.all()
        return tasks

    @action(detail=True, methods=['get'])
    def move_to_in_progress(self, request, *args, **kwargs):
        """Move Task to IN PROGRESS"""
        instance = self.get_object()
        if can_proceed(instance.in_progress):
            instance.in_progress()
            instance.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['put'], serializer_class=serializers.LinkTaskSerializer)
    def link_to_task(self, request, *args, **kwargs):
        """Link Task with another Task"""
        instance = self.get_object()
        if instance.can_link:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


    @action(detail=True, methods=['get'])
    def move_to_done(self, request, *args, **kwargs):
        """Move Task To Done"""
        instance = self.get_object()
        if can_proceed(instance.done):
            instance.done()
            instance.save()
            return Response(status=status.HTTP_200_OK)    
        return Response(status=status.HTTP_403_FORBIDDEN)        