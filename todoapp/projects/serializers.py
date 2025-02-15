from rest_framework import serializers

from projects.models import Project
from users.serializers import ProjectStatsSerializer


class ProjectSerializer (serializers.ModelSerializer):
    existing_member_count = serializers.IntegerField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'status',
                  'existing_member_count', 'max_members']

    def get_status(self, obj):
        CHOICES = ["To be started", "In progress", "Completed"]
        return CHOICES[obj.status]


class ProjectMemberStartsASerializer (serializers.ModelSerializer):
    done = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_name', 'done', 'max_members']

    def get_project_name(self, obj):
        return obj.name

    def get_done(self, obj):
        return False if obj.status < 2 else True


class ProjectReportSerializer (serializers.ModelSerializer):
    report = ProjectStatsSerializer(source='annotated_members', many=True)
    project_title = serializers.CharField(source='name')

    class Meta:
        model = Project
        fields = ['project_title', 'report']
