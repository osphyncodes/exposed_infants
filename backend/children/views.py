from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Change password view for standard users

from django.contrib.auth.models import User
from .forms_user import UserForm

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

from django.contrib.auth.decorators import user_passes_test

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
    return render(request, 'user_management.html', {'users': users})

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
    return render(request, 'change_hcc_number.html', {'form': form, 'child': child, 'error': error})

@login_required
def dashboard(request):
    total_children = Child.objects.count()
    total_visits = ChildVisit.objects.count()
    total_hts_samples = HTSSample.objects.count()

    recent_children = Child.objects.order_by('-child_dob')[:5]
    recent_visits = ChildVisit.objects.select_related('child').order_by('-visit_date')[:5]

    # Children registered per month (last 6 months)

    children_per_month_qs = (
        Child.objects.annotate(month=TruncMonth('child_dob'))
        .values('month')
        .annotate(count=Count('hcc_number'))
        .order_by('month')
    )
    children_per_month_labels = [c['month'].strftime('%b %Y') if c['month'] else '' for c in children_per_month_qs]
    children_per_month_data = [c['count'] for c in children_per_month_qs]

    # Gender distribution
    gender_qs = Child.objects.values('child_gender').annotate(count=Count('hcc_number'))
    gender_labels = [g['child_gender'] for g in gender_qs]
    gender_data = [g['count'] for g in gender_qs]

    context = {
        'total_children': total_children,
        'total_visits': total_visits,
        'total_hts_samples': total_hts_samples,
        'recent_children': recent_children,
        'recent_visits': recent_visits,
        'children_per_month_labels': json.dumps(children_per_month_labels),
        'children_per_month_data': json.dumps(children_per_month_data),
        'gender_labels': json.dumps(gender_labels),
        'gender_data': json.dumps(gender_data),
    }
    return render(request, 'dashboard.html', context)

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
            form.save()
            return redirect('children:children')
    else:
        form = ChildForm()
    return render(request, 'add_child.html', {'form': form})

@login_required
def children_view(request):
    children = Child.objects.all()

    if request.method == 'POST':
        search_by = request.POST.get('search_by')
        query = request.POST.get('query')

        if search_by and query:
            if search_by == 'hcc':
                children = children.filter(hcc_number__icontains=query)
            elif search_by == 'mother_art':
                children = children.filter(mother_art_number__icontains=query)

    return render(request, 'children.html', {'children': children})


@login_required
def reports(request):
    return render(request, 'reports.html')


@login_required
def reminders(request):
    return render(request, 'reminders.html')

@login_required
def import_export(request):
    return render(request, 'import_export.html')

@login_required
def logs(request):
    logs = SystemLog.objects.select_related('user').order_by('-timestamp')[:100]
    return render(request, 'logs.html', {'logs': logs})

@login_required
def child_dashboard_view(request, hcc_number):
    child = get_object_or_404(Child, hcc_number=hcc_number)
    visits = child.visits.order_by('-visit_date')
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
    if visits.exists():
        latest_visit = visits.first()
        outcome = latest_visit.follow_up_outcome
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

    return render(request, 'child_dashboard.html', {
        'child': child,
        'visits': visits,
        'child_fields': child_fields,
        'current_outcome': current_outcome,
        'current_outcome_date': current_outcome_date,
        'missed_or_defaulted_date': missed_or_defaulted_date,
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
    return render(request, 'edit_field.html', {
        'child': child,
        'form': form,
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
    return render(request, 'confirm_delete.html', {'child': child})

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
            return redirect('children:child_dashboard', hcc_number=child.hcc_number)
    else:
        form = ChildVisitForm(child=child)

    return render(request, 'add_visit.html', {'form': form, 'child': child, 'show_weight_muac': show_weight_muac})


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

    return render(request, 'add_hts.html', {'form': form, 'child': child})

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
    return render(request, 'add_visit.html', {'form': form, 'child': child, 'show_weight_muac': False, 'outcome_only': True})

@login_required
def app_selector(request):
    return render(request, 'app_selector.html')

