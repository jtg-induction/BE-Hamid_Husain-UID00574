from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import CustomUser


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class StatsSerializer (serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'completed_count', 'pending_count']


class PendingSerializer (serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'pending_count']


class UserProjetSerializer (serializers.ModelSerializer):
    to_do_projects = serializers.SerializerMethodField()
    in_progress_projects = serializers.SerializerMethodField()
    completed_projects = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'to_do_projects',
                  'in_progress_projects', 'completed_projects']

    def get_to_do_projects(self, obj):
        return obj.to_do_projects

    def get_in_progress_projects(self, obj):
        return obj.in_progress_projects

    def get_completed_projects(self, obj):
        return obj.completed_projects


class ProjectStatsSerializer (serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'completed_count', 'pending_count']


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'password', 'confirm_password', 'date_joined']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and Confirm Password do not match.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
