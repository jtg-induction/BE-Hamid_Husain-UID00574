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
        CHOICES = ["To be started", "In Progress", "Completed"]
        return CHOICES[obj.status]


class ProjectMemberStartsASerializer (serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'status', 'max_members']

    def get_status(self, obj):
        CHOICES = ["To be started", "In Progress", "Completed"]
        return CHOICES[obj.status]


class ProjectReportSerializer (serializers.ModelSerializer):
    report = ProjectStatsSerializer(source='annotated_members', many=True)
    project_title = serializers.CharField(source='name')

    class Meta:
        model = Project
        fields = ['project_title', 'report']
