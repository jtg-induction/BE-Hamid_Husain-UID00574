import json
from datetime import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, Q, Prefetch

from projects.models import Project
from projects.serializers import ProjectSerializer, ProjectReportSerializer, ProjectMemberStartsASerializer
from todos.models import Todo
from todos.serializers import TodoSerializer, TodoDateSerializer
from users.models import CustomUser
from users.serializers import UserSerializer, PendingSerializer, StatsSerializer, UserProjetSerializer


def fetch_all_users():
    """
    Util to fetch given user's tod list
    :return: list of dicts - List of users data
    """
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_all_todo_list_with_user_details():
    """
    Util to fetch given user's tod list
    :return: list of dicts - List of todos
    """
    todos = Todo.objects.all().select_related('user')
    serializer = TodoSerializer(todos, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_projects_details():
    projects = Project.objects.annotate(
        existing_member_count=Count('members')
    )
    serializer = ProjectSerializer(projects, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_users_todo_stats():
    """
    Util to fetch todos list stats of all users on platform
    :return: list of dicts -  List of users with stats
    """
    users = CustomUser.objects.annotate(
        completed_count=Count('todos', filter=Q(todos__done=True)),
        pending_count=Count('todos', filter=Q(todos__done=False))
    )
    serializer = StatsSerializer(users, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_five_users_with_max_pending_todos():
    """
    Util to fetch top five user with maximum number of pending todos
    :return: list of dicts -  List of users
    """
    users = CustomUser.objects.annotate(
        pending_count=Count('todos', filter=Q(todos__done=False))
    )
    top_5_pending = users.order_by('-pending_count')[:5]

    serializer = PendingSerializer(top_5_pending, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_users_with_n_pending_todos(n):
    """
    Util to fetch top five user with maximum number of pending todos
    :param n: integer - count of pending todos
    :return: list of dicts -  List of users
    """
    users = CustomUser.objects.annotate(
        pending_count=Count('todos', filter=Q(todos__done=False))
    )
    pending = users.filter(pending_count=n)

    serializer = PendingSerializer(pending, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_completed_todos_with_in_date_range(start, end):
    """
    Util to fetch todos that were created in between given dates and marked as done.
    :param start: string - Start date e.g. (12-01-2021)
    :param end: string - End date e.g. (12-02-2021)
    :return: list of dicts - List of todos
    """
    start_date = datetime.strptime(start, "%d-%m-%Y")
    end_date = datetime.strptime(end, "%d-%m-%Y")
    todos = Todo.objects.select_related('user').filter(
        date_created__range=[start_date, end_date],
        done=True
    )
    serializer = TodoDateSerializer(todos, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_project_with_member_name_start_or_end_with_a():
    """
    Util to fetch project details having members who have name either starting with A or ending with A.
    :return: list of dicts - List of project data
    """
    projects = Project.objects.filter(
        Q(members__first_name__istartswith='A') | Q(
            members__last_name__iendswith='A')
    ).distinct()

    serializer = ProjectMemberStartsASerializer(projects, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_project_wise_report():
    """
    Util to fetch project wise todos pending &  count per user.
    :return: list of dicts - List of report data
    """
    custom_user_annotation = CustomUser.objects.annotate(
        completed_count=Count('todos', filter=Q(todos__done=True)),
        pending_count=Count('todos', filter=Q(todos__done=False))
    )

    project = Project.objects.prefetch_related(
        Prefetch('members', queryset=custom_user_annotation.order_by(
            'email'), to_attr='annotated_members')
    ).all()
    serializer = ProjectReportSerializer(project, many=True)
    return json.loads(json.dumps(serializer.data))


def fetch_user_wise_project_status():
    """
    Util to fetch user wise project statuses.
    :return: list of dicts - List of user project data
    """
    user = CustomUser.objects.annotate(
        to_do_projects=ArrayAgg(
            'projectmember__project__name',
            filter=Q(projectmember__project__status=0)
        ),
        in_progress_projects=ArrayAgg(
            'projectmember__project__name',
            filter=Q(projectmember__project__status=1)
        ),
        completed_projects=ArrayAgg(
            'projectmember__project__name',
            filter=Q(projectmember__project__status=2)
        )
    )

    serializer = UserProjetSerializer(user, many=True)
    return json.loads(json.dumps(serializer.data))
