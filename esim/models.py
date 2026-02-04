from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Plan(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100)


class UserPlanMapping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_plan_mappings"
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="user_plan_mappings"
    )
    request_id = models.IntegerField(unique=True)
    