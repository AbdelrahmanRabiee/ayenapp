from rest_framework import serializers

from django.contrib.auth import password_validation

from users.models import User, UserFiles


class UserAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name']


class UserFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFiles
        fields = ['id', 'name', 'file']

    def save(self, owner):
        name = self.validated_data.get('name')
        file = self.validated_data.get('file')
        UserFiles.objects.create(user=owner, name=name, file=file)
            