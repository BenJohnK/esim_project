from rest_framework import serializers
from .models import User, Plan, UserPlanMapping

class UserPlanMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlanMapping
        fields = ["user", "plan", "request_id"]


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["all"]