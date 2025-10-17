from .models import Tracing, PhoneTracing, HomeTracing  # or wherever you store notifications
from django.db.models import Max, OuterRef, Subquery, DateTimeField
from datetime import date, timedelta
from django.db.models.functions import Greatest
from django.utils.timezone import now
from django.utils import timezone

def notification_count(request):
    tracings = Tracing.objects.all()

    count = 0
    art_number = 44
    

    # count of clients without phone
    no_phone = tracings.filter(with_phone=True, phone_called=False).all()
    no_phone_count = no_phone.count()

    overdue = []
    need_closure = []
    tracing_overdue = []
    recent_talked_date = None
    days_since_contact = 0
    now = timezone.now()
    tracing_overdue_count = 0
    need_closure_count = 0

    for tracing in tracings:
        # Client talked to 14+ days ago but not yet come
        if tracing.tracing_outcome and tracing.final_outcome == '':
            recent_talked_date = None

            # Latest home contact
            recent_home = tracing.home_tracings.filter(outcome='found_house_talked').order_by('-date_visited').first()
            recent_home_date = recent_home.date_visited if recent_home else None

            # Latest phone contact
            recent_phone = tracing.phone_tracings.filter(outcome='talked_to_client').order_by('-date_called').first()
            recent_phone_date = recent_phone.date_called if recent_phone else None

            # Pick the most recent one (if any exist)
            if recent_home_date and recent_phone_date:
                recent_talked_date = max(recent_home_date, recent_phone_date)
            elif recent_home_date:
                recent_talked_date = recent_home_date
            elif recent_phone_date:
                recent_talked_date = recent_phone_date

            if recent_talked_date:

                days_since_contact = (now - recent_talked_date).days
                if days_since_contact > 14:
                    count += 1
                    overdue.append(tracing)

        # Clients without outcome 28+ days after tracing
        days_since_assigned = (now - tracing.date_entered).days

        if tracing.final_outcome == '' or tracing.final_outcome == None:
            
            if days_since_assigned > 28:
                count += 1
                need_closure_count += 1
                need_closure.append(tracing)


        # Clients without tracing 5 days after assignment

        home_count = tracing.home_tracings.count()
        phone_count = tracing.phone_tracings.count()

        if days_since_assigned > 4 and tracing.final_outcome != 'Came Back':
            if home_count == 0 and phone_count == 0:
                count += 1
                tracing_overdue_count += 1
                tracing_overdue.append(tracing)


    count += no_phone_count

    return {
        "notification_count": count,
        'art_number': days_since_contact,
        'overdue_clients':tracing_overdue,
        'tracing_overdue': tracing_overdue,
        'no_phone_clients': no_phone,
        'tracing_overdue_count': tracing_overdue_count,
        'need_closure': need_closure,
        'need_closure_count': need_closure_count
    }



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

