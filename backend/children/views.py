from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Change password view for standard users

from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from .forms_user import UserForm
from django.core.paginator import Paginator
from django.db.models.functions import TruncDay
from django.db.models import OuterRef, Subquery

from .forms_change_hcc import ChangeHCCNumberForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ChildForm, ChildVisitForm, HTSSampleForm
from .forms_outcome import OutcomeVisitForm
from .models import Child, ChildVisit, HTSSample, SystemLog
from django.forms.models import model_to_dict
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json
from django.http import JsonResponse

from django.utils import timezone

from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

def is_superuser(user):
    return user.is_superuser

@login_required
def change_password(request):
    from django.contrib import messages
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was changed successfully.')
            return redirect('children:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def user_management(request):
    users = User.objects.all()
    return render(request, 'children/user_management.html', {'users': users})

@login_required
@user_passes_test(is_superuser)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('children:user_management')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form, 'action': 'Add'})

@login_required
@user_passes_test(is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('children:user_management')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form, 'action': 'Edit'})

@login_required
@user_passes_test(is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('children:user_management')
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
def change_hcc_number(request, hcc_number):
    child = get_object_or_404(Child, hcc_number=hcc_number)
    error = None
    if request.method == 'POST':
        form = ChangeHCCNumberForm(request.POST)
        if form.is_valid():
            new_hcc = form.cleaned_data['new_hcc_number']
            if Child.objects.filter(hcc_number=new_hcc).exists():
                error = 'A child with this HCC Number already exists.'
            else:
                from django.db import transaction, connection
                old_hcc = child.hcc_number
                with transaction.atomic():
                    # Update PK using raw SQL
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE children_child SET hcc_number = %s WHERE hcc_number = %s",
                            [new_hcc, old_hcc]
                        )
                    # Update all related records to point to the new PK (by value)
                    ChildVisit.objects.filter(child__hcc_number=new_hcc).update(child_id=new_hcc)
                    HTSSample.objects.filter(child__hcc_number=new_hcc).update(child_id=new_hcc)
                return redirect('children:child_dashboard', hcc_number=new_hcc)
    else:
        form = ChangeHCCNumberForm(initial={'new_hcc_number': child.hcc_number})
    return render(request, 'children/change_hcc_number.html', {'form': form, 'child': child, 'error': error})

@login_required
def dashboard(request):
    current_year = date.today().year
    start_year = current_year - 2

    current_year_str = date(current_year, 12, 31)
    start_year_str = date(start_year, 1, 1)

    total_children = Child.objects.filter(child_dob__year__range=(start_year, current_year)).count()

    # Get latest visits for each child
    latest_visits = ChildVisit.objects.filter(
        child__child_dob__year__range=(start_year, current_year),
        child=OuterRef('pk')
        )
    
    # Annotate children with their latest visit date
    # This will give us the latest visit date for each child
    children_with_latest_visits = Child.objects.annotate(
        latest_visit_date=Subquery(
            latest_visits.filter().values('next_appointment_or_outcome_date').order_by('-next_appointment_or_outcome_date')[:1]
        ),
        current_outcome=Subquery(
            latest_visits.filter().values('follow_up_outcome').order_by('-next_appointment_or_outcome_date')[:1]
        )
    )

    outcomeCount = 0
    defaultedPepfarCount = 0
    defaultedMOHCount = 0
    missedCount = 0
    aliveCount = 0
    diedCount = 0
    toCount = 0
    disCount = 0
    artCount = 0
    noCount = 0


    # Initialize counts
    # Iterate through children to determine their current outcome based on latest visit date
    for child in children_with_latest_visits:
        if child.current_outcome == 'Con':
            if child.latest_visit_date:
                days_since = (timezone.now().date() - child.latest_visit_date).days
                if days_since > 60:
                    child.current_outcome = 'Defaulted'
                    defaultedMOHCount += 1
                elif days_since > 28:
                    defaultedPepfarCount += 1
                elif days_since > 7:
                    child.current_outcome = 'Missed Appointment'
                    missedCount += 1
                else:
                    child.current_outcome = 'Alive in Care'
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
            print(child.hcc_number)
        outcomeCount += 1
    
    outcomeData = [
        defaultedMOHCount + defaultedPepfarCount,
        missedCount,
        aliveCount,
        diedCount,
        toCount,
        disCount,
        artCount,
        noCount
    ]
    
    totalCheck= total_children - (defaultedPepfarCount + defaultedMOHCount + missedCount + aliveCount + diedCount + toCount + disCount + artCount)
    if totalCheck > 0:
        print(f"Warning: There are {totalCheck} children with outcomes not accounted for in the counts.")
    print(f"Total children with outcomes: {outcomeCount}, Defaulted: {defaultedMOHCount + defaultedPepfarCount}, Missed: {missedCount}, Alive: {aliveCount} died: {diedCount}, Transferred Out: {toCount}, Discharged: {disCount}, Started ART: {artCount}")

    total_visits = children_with_latest_visits.exclude(latest_visit_date=None).count()

    total_hts_samples = HTSSample.objects.count()


    # Upcoming appointments (next 7 days)
    today = timezone.now().date()
    upcoming_appointments = ChildVisit.objects.filter(
        next_appointment_or_outcome_date__gte=today,
        next_appointment_or_outcome_date__lte=today + timedelta(days=7)
    ).count()

    # Recent records
    recent_children = Child.objects.order_by('-child_dob').filter(child_dob__year__range=(start_year, current_year))[:5]
    recent_visits = ChildVisit.objects.select_related('child').order_by('-visit_date')[:5]

    # Children registered per month (last 12 months)
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

    # Gender distribution
    gender_distribution = (
        Child.objects.values('child_gender')
        .annotate(count=Count('hcc_number'))
        .order_by('child_gender')
    )
    gender_labels = [g['child_gender'] for g in gender_distribution]
    gender_data = [g['count'] for g in gender_distribution]

    # Visit trends (last 7 days)
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

    visit_trends_labels = [v['day'].strftime('%a %d %b') for v in visit_trends]  # e.g., "Mon 08 Jul"
    visit_trends_data = [v['total_visits'] for v in visit_trends]
    unique_children_trends_data = [v['unique_children'] for v in visit_trends]

        # Visit trends (next 7 days)
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


    # Outcomes distribution
    outcomes = (
        ChildVisit.objects.values('follow_up_outcome')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    outcome_labels = [o['follow_up_outcome'] for o in outcomes]
    outcome_data = [o['count'] for o in outcomes]

    # Last 7 days visits
    seven_days_ago = today - timedelta(days=6)
    visits_last_7_days = (
        ChildVisit.objects.filter(visit_date__gte=seven_days_ago)
        .select_related('child')
        .order_by('-visit_date')
    )
    unique_children_count = visits_last_7_days.values('child').distinct().count()

    # Wasting statistics
    wasting_stats = (
        ChildVisit.objects.values('wasting')
        .annotate(count=Count('id'))
        .order_by('wasting')
    )

    childrens = Child.objects.filter(child_dob__year=2023).values('child_name', 'child_dob', 'hcc_number')
    print("Children born in 2024:")
    print(childrens.count())

    context = {
        'current_year': current_year,
        'start_year': start_year,
        'total_children': total_children,
        'total_visits': total_visits,
        'total_hts_samples': total_hts_samples,
        'upcoming_appointments': upcoming_appointments,
        'recent_children': recent_children,
        'recent_visits': recent_visits,
        'visits': visits_last_7_days,
        'unique_children_count': unique_children_count,

        # outcomes count
        'aliveCount': aliveCount,
        'tiPepfar': defaultedPepfarCount,
        'tiMOH': defaultedMOHCount,
        'outcomeData': outcomeData,
        
        # Chart data
        'children_per_month_labels': json.dumps(children_per_month_labels),
        'children_per_month_data': json.dumps(children_per_month_data),
        'gender_labels': json.dumps(gender_labels),
        'gender_data': json.dumps(gender_data),
        'visit_trends_labels': json.dumps(visit_trends_labels),
        'visit_trends_data': json.dumps(visit_trends_data),
        'unique_children_trends_data': json.dumps(unique_children_trends_data),
        'outcome_labels': json.dumps(outcome_labels),
        'outcome_data': json.dumps(outcome_data),
        'wasting_stats': wasting_stats,
        'app_trends_labels': json.dumps(app_trends_labels),
        'app_trends_data': json.dumps(app_trends_data),
    }
    return render(request, 'children/dashboard.html', context)

@login_required
def children_view(request):
    return render(request, 'children.html')

@login_required
def add_child(request):
    from django.contrib import messages
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to add a child.')
        return redirect('children:dashboard')
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save()
            return redirect('children:child_dashboard', hcc_number=child.hcc_number)
    else:
        form = ChildForm()
    return render(request, 'children/add_child.html', {'form': form})

@login_required
def children_view(request):
    if request.method == 'POST':
        children = Child.objects.all().values()

        return JsonResponse(list(children), safe=False)
    
@login_required
def children_views(request):
    children_list = Child.objects.all()

    # Handle search
    if request.method == 'POST':
        search_by = request.POST.get('search_by')
        query = request.POST.get('query')
        if search_by and query:
            if search_by == 'hcc':
                children_list = children_list.filter(hcc_number__icontains=query)
            elif search_by == 'mother_art':
                children_list = children_list.filter(mother_art_number__icontains=query)

    # Get per_page from GET
    per_page = request.GET.get('per_page', '10')

    if per_page == 'all':
        page_obj = children_list  # Not paginated
        is_paginated = False
    else:
        try:
            per_page = per_page
        except ValueError:
            per_page = '10'
            # per_page = 10
        paginator = Paginator(children_list, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        is_paginated = True

    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'is_paginated': is_paginated,
    }
    return render(request, 'children/children.html', context)

@login_required
def reports(request):
    return render(request, 'children/reports.html')

@login_required
def reminders(request):
    return render(request, 'children/reminders.html')

@login_required
def import_export(request):
    return render(request, 'children/import_export.html')

@login_required
def logs(request):
    logs = SystemLog.objects.select_related('user').order_by('-timestamp')[:100]
    return render(request, 'children/logs.html', {'logs': logs})

@login_required
def child_dashboard_view(request, hcc_number):
    child = get_object_or_404(Child, hcc_number=hcc_number)
    visits = child.visits.order_by('-visit_date')[:1]
    hts_samples = child.hts_samples.order_by('-sample_date')[:1]
    # Get field names and values
    child_fields = []
    for field in child._meta.fields:
        if field.name != "id":
            child_fields.append({
                'name': field.name,
                'verbose_name': field.verbose_name,
                'value': getattr(child, field.name),
            })

    # Determine current outcome
    current_outcome = None
    current_outcome_date = None
    current_result = None
    art_number = None
    if visits.exists():
        latest_visit = visits.first()
        outcome = latest_visit.follow_up_outcome

        if (latest_visit):
            art_number = latest_visit.art_number

        outcome_date = latest_visit.next_appointment_or_outcome_date
        from datetime import date, timedelta
        today = date.today()
        missed_or_defaulted_date = None

        if outcome == 'Con':  # Continue FUP
            if outcome_date:
                days_since = (today - outcome_date).days
                if days_since > 28:
                    current_outcome = 'Defaulted'
                    missed_or_defaulted_date = outcome_date + timedelta(days=29)
                elif days_since > 7:
                    current_outcome = 'Missed Appointment'
                    missed_or_defaulted_date = outcome_date + timedelta(days=8)
                else:
                    current_outcome = 'Alive in Care'
                current_outcome_date = outcome_date
            else:
                current_outcome = 'Alive in Care'
                current_outcome_date = None
        else:
            # Show the most recent outcome and date
            current_outcome = latest_visit.get_follow_up_outcome_display()
            current_outcome_date = outcome_date
        # If missed_or_defaulted_date is set, pass it
    else:
        missed_or_defaulted_date = None

    if hts_samples.exists():
        latest_hts = hts_samples.first()
        hts_result = latest_hts.result
        hts_date_received = latest_hts.date_received
        if hts_result:
            current_result = latest_hts.result
        else:
            current_result = 'Pending'
    else:
        current_result = 'No HTS Samples'


    return render(request, 'children/child_dashboard.html', {
        'child': child,
        'art_number': art_number,
        'hts_samples': hts_samples,
        'visits': visits,
        'child_fields': child_fields,
        'current_outcome': current_outcome,
        'current_outcome_date': current_outcome_date,
        'missed_or_defaulted_date': missed_or_defaulted_date,
        'current_result': current_result,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_child_field_view(request, hcc_number, field=None):
    child = get_object_or_404(Child, hcc_number=hcc_number)
    from .forms import ChildForm
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            return redirect('children:child_dashboard', hcc_number=hcc_number)
    else:
        form = ChildForm(instance=child)
    return render(request, 'children/edit_field.html', {
        'child': child,
        'form': form,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_hts_result(request, hcc_number, field=None):
    child = get_object_or_404(Child, hcc_number=hcc_number)
    hts_sample = get_object_or_404(HTSSample, child=child)
    from .forms import HTSSampleForm
    if request.method == 'POST':
        form = HTSSampleForm(request.POST, instance=hts_sample)
        if form.is_valid():
            form.save()
            return redirect('children:child_dashboard', hcc_number=hcc_number)
    else:
        form = HTSSampleForm(instance=hts_sample)

        print(form.initial)
    return render(request, 'edit_hts.html', {
        'child': child,
        'form': form,
    })

@login_required
def view_child_visits(request, hcc_number):
    child = get_object_or_404(Child, hcc_number=hcc_number)
    visits = child.visits.order_by('-visit_date')
    count = visits.count()

    print(count)

    return render(request, 'children/view_visits.html', {
        'child': child,
        'visits': visits,
        'count': count
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_child_view(request, hcc_number):
    child = get_object_or_404(Child, hcc_number=hcc_number)
    if request.method == 'POST':
        child.delete()
        from django.contrib import messages
        messages.success(request, 'Child deleted successfully.')
        return redirect('children:children')
    return render(request, 'children/confirm_delete.html', {'child': child})

@login_required
def add_visit(request, hcc_number):
    from django.contrib import messages
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to add a visit.')
        return redirect('children:dashboard')
    child = get_object_or_404(Child, hcc_number=hcc_number)

    from datetime import date
    # Calculate age in months at visit date (default to today if not provided)
    visit_date = None
    if request.method == 'POST':
        visit_date = request.POST.get('visit_date')
    if not visit_date:
        visit_date = date.today()
    else:
        try:
            visit_date = date.fromisoformat(visit_date)
        except Exception:
            visit_date = date.today()
    age_months = (visit_date.year - child.child_dob.year) * 12 + (visit_date.month - child.child_dob.month)
    show_weight_muac = age_months >= 6

    if request.method == 'POST':
        form = ChildVisitForm(request.POST, child=child)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.child = child
            visit.save()
            return redirect('children:view_visits', hcc_number=child.hcc_number)
    else:
        form = ChildVisitForm(child=child)

    return render(request, 'children/add_visit.html', {'form': form, 'child': child, 'show_weight_muac': show_weight_muac})

@login_required
def add_hts_result(request, hcc_number):
    from django.contrib import messages
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to add an HTS sample.')
        return redirect('children:dashboard')
    child = get_object_or_404(Child, hcc_number=hcc_number)

    if request.method == 'POST':
        form = HTSSampleForm(request.POST, child=child)  # pass child here
        if form.is_valid():
            form.save()
            return redirect('children:child_dashboard', hcc_number=child.hcc_number)
    else:
        form = HTSSampleForm(child=child)  # also pass child on GET

    return render(request, 'children/add_hts.html', {'form': form, 'child': child})

@login_required
def update_outcome(request, hcc_number):
    from django.contrib import messages
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to update outcome information.')
        return redirect('children:dashboard')
    child = get_object_or_404(Child, hcc_number=hcc_number)
    if request.method == 'POST':
        form = OutcomeVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.child = child
            visit.save()
            return redirect('children:child_dashboard', hcc_number=child.hcc_number)
    else:
        form = OutcomeVisitForm()
    return render(request, 'children/add_visit.html', {'form': form, 'child': child, 'show_weight_muac': False, 'outcome_only': True})

@login_required
def app_selector(request):
    return render(request, 'children/app_selector.html')

from django.contrib import messages

def delete_visit(request, visit_id):
    visit = get_object_or_404(ChildVisit, id=visit_id)

    hcc_number = request.POST.get('hcc_number')

    if request.method == 'POST':
        visit.delete()
        messages.success(request, 'Visit deleted successfully.')
    return redirect('children:view_visits', hcc_number = hcc_number) 


@login_required
def defaulters(request):

    context = {
        'title':  'Defaulters Report',
        'what': 'Def',
        'date_what': 'Date Defaulted'
    }
    return render(request, 'children/reports/defaulters.html', context)

@login_required
def missed(request):

    context = {
        'title':  'Missed Appointment Report',
        'what': 'MA',
        'date_what': 'Date Became Missed'
    }
    return render(request, 'children/reports/defaulters.html', context)
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def defaulters_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            start_date_str = data.get('start_date')
            end_date_str = data.get('end_date')

            # Validate and parse dates
            try:
                start_date = parse_date(start_date_str)
                end_date = parse_date(end_date_str)
            except Exception:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

            if not start_date or not end_date:
                return JsonResponse({'error': 'Start and end dates are required'}, status=400)

            defaulters = []
            missed=[]

            missedCount = 0
            defCount = 0

            today = date.today()
            delta_days = delta_days = (today - start_date).days 

            print(f"date difference is {delta_days}")


            for child in Child.objects.all():
                latest_visit = child.visits.order_by('-visit_date').first()

                if latest_visit and latest_visit.follow_up_outcome == 'Con':
                    appointment_date = latest_visit.next_appointment_or_outcome_date
                    days_since = (timezone.now().date() - appointment_date).days
                    
                    if 7 < days_since <= 27:
                        if appointment_date:
                            defaulting_date = appointment_date + timedelta(days=7)

                            # Check if defaulting_date is within the filter range
                            if start_date <= defaulting_date <= end_date:
                                missedCount += 1
                                missed.append({
                                    'hcc_number': child.hcc_number,
                                    'child_name': child.child_name,
                                    'child_gender': child.child_gender,
                                    'child_dob': child.child_dob,
                                    'guardian_name': child.guardian_name,
                                    'relationship': child.relationship,
                                    'guardian_phone': child.guardian_phone,
                                    'physical_address': child.physical_address,
                                    'mother_status': child.mother_status,
                                    'mother_art_number': child.mother_art_number,
                                    'mother_art_start_date': child.mother_art_start_date,
                                    'defaulting_date': defaulting_date,
                                    'view_url': f"/children/exposed/children/child_dashboard/{child.hcc_number}/"
                                })
                    else:
                        if appointment_date:
                            defaulting_date = appointment_date + timedelta(days=28)

                            # Check if defaulting_date is within the filter range
                            if start_date <= defaulting_date <= end_date:
                                defCount += 1
                                defaulters.append({
                                    'hcc_number': child.hcc_number,
                                    'child_name': child.child_name,
                                    'child_gender': child.child_gender,
                                    'child_dob': child.child_dob,
                                    'guardian_name': child.guardian_name,
                                    'relationship': child.relationship,
                                    'guardian_phone': child.guardian_phone,
                                    'physical_address': child.physical_address,
                                    'mother_status': child.mother_status,
                                    'mother_art_number': child.mother_art_number,
                                    'mother_art_start_date': child.mother_art_start_date,
                                    'defaulting_date': defaulting_date,
                                    'view_url': f"/children/exposed/children/child_dashboard/{child.hcc_number}/"
                                })
            response = {
                'count': defCount,
                'missedCount': missedCount,
                'defaulters': defaulters,
                'missed_apps': missed
            }

            return JsonResponse(response, encoder=DjangoJSONEncoder)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required
def appointments(request):

    context = {
        'what': "App",
        'date_what': "Appointment Date",
        'title': "Appointment Report"
    }
    return render(request, 'children/reports/appointments.html', context=context)

@require_POST
def appointments_view(request):
    try:
        data = json.loads(request.body)
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        # Validate and parse dates
        try:
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        if not start_date or not end_date:
            return JsonResponse({'error': 'Start and end dates are required'}, status=400)

        appointments = []

        # Get all children with latest visit outcome = 'Con'
        children = Child.objects.annotate(
            latest_visit_date=Max('visits__visit_date')
        ).filter(
            visits__follow_up_outcome='Con',
            visits__next_appointment_or_outcome_date__range=(start_date, end_date)
        ).distinct()

        for child in children:
            latest_visit = child.visits.order_by('-visit_date').first()
            if not latest_visit or not latest_visit.next_appointment_or_outcome_date:
                continue

            appointment_date = latest_visit.next_appointment_or_outcome_date
            dob = child.child_dob
            
            # Calculate age in months at appointment date
            delta = relativedelta(appointment_date, dob)
            age_in_months = delta.years * 12 + delta.months

            action_needed = None
            hts_test_required = False
            hts_test_reason = None

            # Determine required tests based on age
            if age_in_months >= 24:
                # Check for Rapid @ 2yr test
                hts_test_reason = 'Rapid_2yr'
                if not child.hts_samples.filter(reason='Rapid_2yr').exists():
                    hts_test_required = True
                    action_needed = 'Needs Rapid Test @ 2 years'
            elif age_in_months >= 12:
                # Check for Rapid @ 1yr test
                hts_test_reason = 'Rapid_1yr'
                if not child.hts_samples.filter(reason='Rapid_1yr').exists():
                    hts_test_required = True
                    action_needed = 'Needs Rapid Test @ 1 year'
            elif age_in_months >= 1.5:  # 6 weeks = ~1.5 months
                # Check for DBS 6 weeks test
                hts_test_reason = 'DBS_6wks_Ini'
                if not child.hts_samples.filter(reason='DBS_6wks_Ini').exists():
                    hts_test_required = True
                    action_needed = 'Needs DBS 6 Weeks Initial Test'
            else:
                action_needed = 'No HTS test required at this age'

            appointments.append({
                'hcc_number': child.hcc_number,
                'child_name': child.child_name,
                'child_dob': child.child_dob,
                'child_gender': child.child_gender,
                'guardian_name': child.guardian_name,
                'guardian_phone': child.guardian_phone,
                'physical_address': child.physical_address,
                'appointment_date': appointment_date,
                'age_in_months': age_in_months,
                'hts_test_required': hts_test_required,
                'hts_test_reason': hts_test_reason,
                'action_needed': action_needed,
                'mother_status': child.mother_status,
                'mother_art_number': child.mother_art_number,
                'view_url': f"/children/exposed/children/child_dashboard/{child.hcc_number}/"
            })

        return JsonResponse({
            'count': len(appointments),
            'appointments': appointments
        }, encoder=DjangoJSONEncoder)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def missed_milestones_view(request):
    if request.method == 'GET':
        return render(request, 'children/reports/missed_milestone.html')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            birth_year = data.get('birth_year')
            reason = data.get('reason')
            
            today = date.today()
            children = Child.objects.all()
            
            if birth_year:
                children = children.filter(child_dob__year=birth_year)
            
            missed_milestones = []
            
            for child in children:
                dob = child.child_dob
                age_months = (today.year - dob.year) * 12 + (today.month - dob.month)
                
                # Determine expected tests
                required_tests = []
                if age_months >= 1.5:  # 6 weeks
                    required_tests.append(('DBS_6wks_Ini', dob + timedelta(weeks=6)))
                if age_months >= 12:
                    required_tests.append(('Rapid_1yr', dob + timedelta(days=365)))
                if age_months >= 24:
                    required_tests.append(('Rapid_2yr', dob + timedelta(days=730)))
                
                # Check for missing tests
                for test_reason, due_date in required_tests:
                    if reason and test_reason != reason:
                        continue
                        
                    if not child.hts_samples.filter(reason=test_reason).exists():
                        days_overdue = (today - due_date).days
                        if days_overdue > 0:
                            missed_milestones.append({
                                'hcc_number': child.hcc_number,
                                'child_name': child.child_name,
                                'child_dob': child.child_dob,
                                'age_months': age_months,
                                'guardian_name': child.guardian_name,
                                'guardian_phone': child.guardian_phone,
                                'test_reason': test_reason,
                                'due_date': due_date,
                                'days_overdue': days_overdue,
                                'view_url': f"/children/exposed/children/child_dashboard/{child.hcc_number}/"
                            })
            
            # Get unique birth years for filter (modified to ensure uniqueness)
            birth_years = Child.objects.dates('child_dob', 'year')\
                          .order_by('-child_dob')\
                          .values_list('child_dob__year', flat=True)\
                          .distinct()
            
            return JsonResponse({
                'missed_milestones': missed_milestones,
                'birth_years': get_recent_years()  # Convert QuerySet to list
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
def get_recent_years():
    current_year = date.today().year
    return [year for year in range(current_year, current_year - 4, -1)]

@login_required()
def eid_report(request):
    if request.method == 'GET':
        return render(request, 'children/reports/eid_report.html')
    
    if request.method == 'POST':
        data = json.loads(request.body)

        cohort2Date = data.get('cohort2Date')
        cohort12Date = data.get('cohort12Date')
        cohort24Date = data.get('cohort24Date')

        count1 = getcount(cohort2Date)
        count2 = getcount(cohort12Date)
        count3 = getcount(cohort24Date)

        return JsonResponse({
            'count1': count1,
            'count2': count2,
            'count3': count3,
            'message': 'Recieved'
        })

def getcount(dateobject):
    start_date = date.fromisoformat(dateobject['firstDate'])
    last_date = date.fromisoformat(dateobject['lastDate'])

    children = Child.objects.filter(child_dob__range = (start_date, last_date))
    
    return children.count()