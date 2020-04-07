from collections import OrderedDict

from rest_framework import serializers

from task_management.models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'related_to', 'created']
        extra_kwargs = {
            'status': {'read_only': True},
            'related_to': {'read_only': True},
            'created': {'read_only': True},
            }

    def get_status(self, obj):
        if obj.status == 0:
            return 'NEW'
        elif obj.status == 1:
            return 'IN PROGRESS'
        else:
            return 'DONE'                


    def save(self, owner=None, **kwargs):
        if owner:
            self.validated_data['owner'] = owner
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
        else:
            self.instance = self.create(validated_data)

        return self.instance   


class LinkTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['related_to', ]