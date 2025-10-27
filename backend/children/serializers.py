# serializers.py
from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    current_year = serializers.IntegerField()
    start_year = serializers.IntegerField()
    total_children = serializers.IntegerField()
    total_visits = serializers.IntegerField()
    total_hts_samples = serializers.IntegerField()
    upcoming_appointments = serializers.IntegerField()
    unique_children_count = serializers.IntegerField()

    # Outcome counts
    aliveCount = serializers.IntegerField()
    tiPepfar = serializers.IntegerField()
    tiMOH = serializers.IntegerField()
    outcomeData = serializers.ListField(child=serializers.IntegerField())

    # Chart data
    children_per_month_labels = serializers.ListField(child=serializers.CharField())
    children_per_month_data = serializers.ListField(child=serializers.IntegerField())
    gender_labels = serializers.ListField(child=serializers.CharField())
    gender_data = serializers.ListField(child=serializers.IntegerField())
    visit_trends_labels = serializers.ListField(child=serializers.CharField())
    visit_trends_data = serializers.ListField(child=serializers.IntegerField())
    unique_children_trends_data = serializers.ListField(child=serializers.IntegerField())
    outcome_labels = serializers.ListField(child=serializers.CharField())
    outcome_data = serializers.ListField(child=serializers.IntegerField())
    app_trends_labels = serializers.ListField(child=serializers.CharField())
    app_trends_data = serializers.ListField(child=serializers.IntegerField())
