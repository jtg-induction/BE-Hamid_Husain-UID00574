from django.conf import settings
from django.db import models
from users.models import CustomUser

TO_BE_STARTED = 0
IN_PROGRESS = 1
COMPLETED = 2


class Project(models.Model):
    members = models.ManyToManyField(
        CustomUser, through='ProjectMember', related_name='projects')
    name = models.CharField(max_length=100)
    max_members = models.PositiveIntegerField()

    class status(enumerate):
        TO_BE_STARTED = 0
        IN_PROGRESS = 1
        COMPLETED = 2

    CHOICES = [
        (status.TO_BE_STARTED, "To be started"),
        (status.IN_PROGRESS, "In Progress"),
        (status.COMPLETED, "Completed")
    ]

    status = models.IntegerField(choices=CHOICES, default=status.TO_BE_STARTED)

    def __str__(self):
        return f"{self.name}"

    """
        Needed fields
        - members (m2m field to CustomUser; create through table and enforce unique constraint for user and project)
        - name (max_length=100)
        - max_members (positive int)
        - status (choice field integer type :- 0(To be started)/1(In progress)/2(Completed), with default value been 0)

        Add string representation for this model with project name.
    """


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "member"], name="unique_project_member")
        ]

    def __str__(self):
        return f"{self.project} {self.member.email}"

    """
    Needed fields
    - project (fk to Project model)
    - member (fk to User model - use AUTH_USER_MODEL from settings)
    - Add unique constraints

    Add string representation for this model with project name and user email/first name.
    """
