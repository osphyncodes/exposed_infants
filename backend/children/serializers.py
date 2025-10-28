# serializers.py
from rest_framework import serializers
from .models import Child, ChildVisit, HTSSample

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

class VisitSerializer(serializers.ModelSerializer):
    age_in_months = serializers.SerializerMethodField()
    
    class Meta:
        model = ChildVisit
        fields = [
            "id",
            "visit_date",
            "height",
            "weight",
            "muac",
            "breastfeeding",
            "wasting",
            "mother_art_status",
            "clinical_monitoring",
            "hiv_testing",
            "infection_status",
            "drug_given",
            "cpt_given",
            "follow_up_outcome",
            "next_appointment_or_outcome_date",
            'age_in_months',
        ]

    def get_age_in_months(self, obj):
        child_dob = obj.child.child_dob
        if child_dob and obj.visit_date:
            return (obj.visit_date.year - child_dob.year) * 12 + (obj.visit_date.month - child_dob.month)
        return None

class HTSSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTSSample
        fields = "__all__"

class ChildSerializers(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)
    hts_samples = HTSSampleSerializer(many=True, read_only=True)# nested serializer

    class Meta:
        model = Child
        fields = "__all__" 
        
