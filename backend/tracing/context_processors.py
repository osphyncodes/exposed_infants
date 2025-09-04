from .models import Tracing, PhoneTracing, HomeTracing  # or wherever you store notifications
from django.db.models import Max, OuterRef, Subquery, DateTimeField
from datetime import date, timedelta
from django.db.models.functions import Greatest
from django.utils.timezone import now

def notification_count(request):
    tracings = Tracing.objects.all()

    count = 0

    # count of clients without phone
    no_phone = tracings.filter(with_phone=True, phone_called=False).all()
    no_phone_count = no_phone.count()

    overCount, overdue_tracings = get_overdue_tracings()

    count += no_phone_count + overCount

    return {"notification_count": count}



def get_overdue_tracings():
    # Subqueries for latest phone/home talked dates
    latest_phone = PhoneTracing.objects.filter(
        tracing=OuterRef('pk'),
        outcome='talked_to_client'
    ).order_by('-date_called').values('date_called')[:1]

    latest_home = HomeTracing.objects.filter(
        tracing=OuterRef('pk'),
        outcome='found_house_talked'
    ).order_by('-date_visited').values('date_visited')[:1]

    # Annotate Tracing with the latest talked date
    tracings = (
        Tracing.objects.filter(tracing_outcome=True, final_outcome__isnull=True)
        .annotate(
            latest_phone=Subquery(latest_phone, output_field=DateTimeField()),
            latest_home=Subquery(latest_home, output_field=DateTimeField()),
        )
        .annotate(
            latest_contact=Greatest('latest_phone', 'latest_home')
        )
        .filter(latest_contact__lte=now() - timedelta(days=14))
    )

    return tracings.count(), list(tracings)

