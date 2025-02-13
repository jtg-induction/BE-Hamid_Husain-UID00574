from rest_framework import serializers

from todos.models import Todo

from users.serializers import UserSerializer


class TodoSerializer (serializers.ModelSerializer):
    creator = UserSerializer(source='user')
    status = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['id', 'name', 'status', 'date_created', 'creator']

    def get_status(self, obj):
        return 'To Do' if not obj.done else 'Done'


class TodoDateSerializer (serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ['id', 'name', 'creator', 'email', 'created_at', 'status']

    def get_status(self, obj):
        return 'To Do' if not obj.done else 'Done'

    def get_creator(self, obj):
        first_name = obj.user.first_name
        last_name = obj.user.last_name
        return first_name+" "+last_name

    def get_email(self, obj):
        return obj.user.email

    def get_created_at(self, obj):
        return obj.date_created.strftime("%I:%M %p, %d %b, %Y")


class TodoCreateSerializer (serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name', 'done', 'date_created', 'user']
