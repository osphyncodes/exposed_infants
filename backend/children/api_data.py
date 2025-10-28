# views.py
from datetime import date, timedelta
from django.db.models import Count, OuterRef, Subquery
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import json

from .models import Child, ChildVisit, HTSSample
from .serializers import DashboardSerializer, ChildSerializers


class DashboardAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        current_year = date.today().year
        start_year = current_year - 2

        total_children = Child.objects.filter(
            child_dob__year__range=(start_year, current_year)
        ).count()

        latest_visits = ChildVisit.objects.filter(
            child__child_dob__year__range=(start_year, current_year),
            child=OuterRef('pk')
        )

        children_with_latest_visits = Child.objects.annotate(
            latest_visit_date=Subquery(
                latest_visits.values('next_appointment_or_outcome_date')
                .order_by('-next_appointment_or_outcome_date')[:1]
            ),
            current_outcome=Subquery(
                latest_visits.values('follow_up_outcome')
                .order_by('-next_appointment_or_outcome_date')[:1]
            )
        )

        defaultedPepfarCount = defaultedMOHCount = missedCount = 0
        aliveCount = diedCount = toCount = disCount = artCount = noCount = 0

        for child in children_with_latest_visits:
            if child.current_outcome == 'Con':
                if child.latest_visit_date:
                    days_since = (timezone.now().date() - child.latest_visit_date).days
                    if days_since > 60:
                        defaultedMOHCount += 1
                    elif days_since > 28:
                        defaultedPepfarCount += 1
                    elif days_since > 7:
                        missedCount += 1
                    else:
                        aliveCount += 1
            elif child.current_outcome == 'Died':
                diedCount += 1
            elif child.current_outcome == 'To':
                toCount += 1
            elif child.current_outcome == 'Dis':
                disCount += 1
            elif child.current_outcome == 'ART':
                artCount += 1
            else:
                noCount += 1

        outcomeData = [
            defaultedMOHCount + defaultedPepfarCount,
            missedCount,
            aliveCount,
            diedCount,
            toCount,
            disCount,
            artCount,
            noCount,
        ]

        today = timezone.now().date()

        total_visits = children_with_latest_visits.exclude(latest_visit_date=None).count()
        total_hts_samples = HTSSample.objects.count()
        upcoming_appointments = ChildVisit.objects.filter(
            next_appointment_or_outcome_date__gte=today,
            next_appointment_or_outcome_date__lte=today + timedelta(days=7)
        ).count()

        twelve_months_ago = today - timedelta(days=365)
        children_per_month = (
            Child.objects.filter(child_dob__gte=twelve_months_ago)
            .annotate(month=TruncMonth('child_dob'))
            .values('month')
            .annotate(count=Count('hcc_number'))
            .order_by('month')
        )
        children_per_month_labels = [c['month'].strftime('%b %Y') for c in children_per_month]
        children_per_month_data = [c['count'] for c in children_per_month]

        gender_distribution = (
            Child.objects.values('child_gender')
            .annotate(count=Count('hcc_number'))
            .order_by('child_gender')
        )
        gender_labels = [g['child_gender'] for g in gender_distribution]
        gender_data = [g['count'] for g in gender_distribution]

        visit_trends = (
            ChildVisit.objects.filter(visit_date__gte=today - timedelta(days=7))
            .annotate(day=TruncDay('visit_date'))
            .values('day')
            .annotate(
                total_visits=Count('id'),
                unique_children=Count('child', distinct=True)
            )
            .order_by('day')
        )

        visit_trends_labels = [v['day'].strftime('%a %d %b') for v in visit_trends]
        visit_trends_data = [v['total_visits'] for v in visit_trends]
        unique_children_trends_data = [v['unique_children'] for v in visit_trends]

        app_trends = (
            ChildVisit.objects.filter(
                next_appointment_or_outcome_date__gte=today,
                next_appointment_or_outcome_date__lte=today + timedelta(days=7)
            )
            .annotate(day=TruncDay('next_appointment_or_outcome_date'))
            .values('day')
            .annotate(total_apps=Count('id'))
            .order_by('day')
        )

        app_trends_labels = [v['day'].strftime('%a %d %b') for v in app_trends]
        app_trends_data = [v['total_apps'] for v in app_trends]

        # Build context for serializer
        context = {
            "current_year": current_year,
            "start_year": start_year,
            "total_children": total_children,
            "total_visits": total_visits,
            "total_hts_samples": total_hts_samples,
            "upcoming_appointments": upcoming_appointments,
            "unique_children_count": children_with_latest_visits.count(),
            "aliveCount": aliveCount,
            "tiPepfar": defaultedPepfarCount,
            "tiMOH": defaultedMOHCount,
            "outcomeData": outcomeData,
            "children_per_month_labels": children_per_month_labels,
            "children_per_month_data": children_per_month_data,
            "gender_labels": gender_labels,
            "gender_data": gender_data,
            "visit_trends_labels": visit_trends_labels,
            "visit_trends_data": visit_trends_data,
            "unique_children_trends_data": unique_children_trends_data,
            "outcome_labels": [],
            "outcome_data": [],
            "app_trends_labels": app_trends_labels,
            "app_trends_data": app_trends_data,
        }

        serializer = DashboardSerializer(context)
        return Response(serializer.data)


class ChildrenListView(generics.ListCreateAPIView):
    serializer_class = ChildSerializers
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Child.objects.all()
        
        search_by = self.request.query_params.get('search_by', '')
        search = self.request.query_params.get('search', '')
        
        if search:
            if search_by == 'hcc':
                queryset = queryset.filter(hcc_number=search)
            else:
                queryset = queryset.filter(mother_art_number=search)
        
        return queryset.order_by('-child_dob')[:10]
    
class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = 'hcc_number'