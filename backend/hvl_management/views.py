import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import HVLRecord, IacSession, DrugResistanceApplication, IacFollowUp
from django.contrib import messages
from pact.models import Staff

def hvl_case_detail(request, sn):
    # Get the HVL record or return 404
    hvl_record = get_object_or_404(HVLRecord, sn=sn)
    result = None
    # Get related data
    iac_sessions = hvl_record.iac_sessions.all().order_by('-session_date')
    iac_follow_ups = hvl_record.iac_follow_ups.all().order_by('-collection_date')
    resistance_tests = hvl_record.drug_resistance_tests.all().order_by('-application_date')
    staffs = Staff.objects.all()

    # iac session count
    iac_session_count = iac_sessions.count()

    iac_followup_count = iac_follow_ups.count()
    
    if iac_follow_ups:
        result = iac_follow_ups.first().result_value

    # check if result is numeric or alphanumeric
    is_numeric = False
    result_value = None
    if result is not None:
        try:
            float(result)
            is_numeric = True
            result_value = float(result)
        except ValueError:
            is_numeric = False
            result_value = result

    context = {
        'hvl_record': hvl_record,
        'iac_sessions': iac_sessions,
        'iac_follow_ups': iac_follow_ups,
        'resistance_tests': resistance_tests,
        'staffs': staffs,
        'iac_session_count': iac_session_count,
        'iac_followup_count': iac_followup_count,
        'is_numeric': is_numeric,
        'result_value': result_value,
    }
    
    return render(request, 'hvl_management/case_detail.html', context)

def add_iac_session(request, sn):
    if request.method == 'POST':
        hvl_record = get_object_or_404(HVLRecord, sn=sn)

        # Check if an IAC session already exists for this HVL record
        if IacSession.objects.filter(hvl_record=hvl_record).exists():
            messages.error(request, 'IAC session already exists for this HVL record.')
            return redirect('hvl_management:hvl_case_detail', sn=sn)
        
        # check if date is not in the future
        session_date = request.POST.get('session_date')
        if session_date and session_date > str(timezone.now().date()):
            messages.error(request, 'Session date cannot be in the future.')
            return redirect('hvl_management:hvl_case_detail', sn=sn)
        
         # Create and save the IAC session
        try:
            session = IacSession(
                hvl_record=hvl_record,
                staff_id=request.POST.get('staff'),  # Assuming staff ID is passed
                session_date=request.POST.get('session_date')
            )
            session.save()
            messages.success(request, 'IAC session added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding IAC session: {str(e)}')
    
    return redirect('hvl_management:hvl_case_detail', sn=sn)

def add_iac_followup(request, sn):
    if request.method == 'POST':
        hvl_record = get_object_or_404(HVLRecord, sn=sn)

        # check if iac session exists for this hvl record
        iac_session = IacSession.objects.filter(hvl_record=hvl_record).first()

        if not iac_session:
            messages.error(request, 'Cannot add follow-up: No IAC session exists for this HVL record.')
            return redirect('hvl_management:hvl_case_detail', sn=sn)
        
        # check if 3 months have passed since the iac session date
        three_months_later = iac_session.session_date + timedelta(days=60)
        if timezone.now().date() < three_months_later:
            messages.error(request, 'Cannot add follow-up: 3 months have not passed since the IAC session date.')
            return redirect('hvl_management:hvl_case_detail', sn=sn)
        
        try:
            follow_up = IacFollowUp(
                hvl_record=hvl_record,
                collection_date=request.POST.get('collection_date'),
                sample_log_number=request.POST.get('sample_log_number'),
                result_value=request.POST.get('result_value') or None,
                date_given_to_client=request.POST.get('date_given_to_client') or None
            )
            follow_up.save()
            messages.success(request, 'IAC follow-up added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding IAC follow-up: {str(e)}')
    
    return redirect('hvl_management:hvl_case_detail', sn=sn)

def add_resistance_test(request, sn):
    if request.method == 'POST':
        hvl_record = get_object_or_404(HVLRecord, sn=sn)

        #  if a resistance test already exists for this hvl record, do not allow another
        if DrugResistanceApplication.objects.filter(hvl_record=hvl_record).exists():
            messages.error(request, 'Drug resistance test already exists for this HVL record.')
            return redirect('hvl_management:hvl_case_detail', sn=sn)
        
        try:
            test = DrugResistanceApplication(
                hvl_record=hvl_record,
                application_date=request.POST.get('application_date'),
                submit_sample=request.POST.get('submit_sample'),
                collection_date=request.POST.get('collection_date') or None,
                resistance_detected=request.POST.get('resistance_detected'),
                action_taken=request.POST.get('action_taken') or None,
                vl_after_action=request.POST.get('vl_after_action') or None,
                comments=request.POST.get('comments') or None
            )
            test.save()
            messages.success(request, 'Drug resistance test added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding drug resistance test: {str(e)}')
    
    return redirect('hvl_management:hvl_case_detail', sn=sn)

def notify_client(request, sn):
    if request.method == 'POST':
        hvl_record = get_object_or_404(HVLRecord, sn=sn)
        iac_follow_ups = IacFollowUp.objects.filter(hvl_record=hvl_record).first()

        if not iac_follow_ups:
            messages.error(request, 'No IAC follow-up exists for this HVL record. Cannot notify client.')
            return redirect('hvl_management:hvl_case_detail', sn=sn)
        
        # check if notification date is not in the future or not before collection date or before hvl_record date entered
        notification_date = request.POST.get('notification_date')
        if notification_date:
            if notification_date > str(timezone.now().date()):
                messages.error(request, 'Notification date cannot be in the future.')
                return redirect('hvl_management:hvl_case_detail', sn=sn)
            if notification_date < str(iac_follow_ups.collection_date):
                messages.error(request, 'Notification date cannot be before the collection date.')
                return redirect('hvl_management:hvl_case_detail', sn=sn)
            if notification_date < str(hvl_record.date_entered):
                messages.error(request, 'Notification date cannot be before the HVL record date entered.')
                return redirect('hvl_management:hvl_case_detail', sn=sn)
        
        # if no result value, cannot notify client
        if iac_follow_ups.result_value is None:
            messages.error(request, 'Cannot notify client: No result value available in the IAC follow-up.')
            return redirect('hvl_management:hvl_case_detail', sn=sn)
        
        # Update the date_given_to_client field
        iac_follow_ups.date_given_to_client = notification_date
        iac_follow_ups.save()

        messages.success(request, f'Client for HVL Record SN: {hvl_record.sn} has been notified successfully!')
    
    return redirect('hvl_management:hvl_case_detail', sn=sn)

def update_result(request, sn):
    if request.method == 'POST':
        hvl_record = get_object_or_404(HVLRecord, sn=sn)
        iac_follow_ups = IacFollowUp.objects.filter(hvl_record=hvl_record).first()
 
        try:
            input_type = request.POST.get('inputType')

            if input_type == 'numeric':
                new_result = request.POST.get('result_numeric')
            elif input_type == 'alphanumeric':
                new_result = request.POST.get('result_alphanumeric')

            if new_result is not None:
                iac_follow_ups.result_value = new_result
                iac_follow_ups.save()
                messages.success(request, 'HVL result updated successfully!')
            else:
                messages.error(request, 'No result value provided.')
        except Exception as e:
            messages.error(request, f'Error updating HVL result: {str(e)}')
    
    return redirect('hvl_management:hvl_case_detail', sn=sn)

def dashboard(request):
    # Get filter parameters from request
    date_filter = request.GET.get('date_range', 'all')
    sex_filter = request.GET.get('sex_filter', 'all')
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    min_result = request.GET.get('min_result')
    max_result = request.GET.get('max_result')
    status_filter = request.GET.get('status_filter', 'all')

    # print filters for debugging
    print(f"Filters - Date: {date_filter}, Sex: {sex_filter}, Min Age: {min_age}, Max Age: {max_age}, Min Result: {min_result}, Max Result: {max_result}, Status: {status_filter}")
    
    # Base queryset
    records = HVLRecord.objects.all()
    
    # Apply filters
    if date_filter != 'all':
        today = timezone.now().date()
        if date_filter == 'today':
            records = records.filter(date_entered=today)
        elif date_filter == 'week':
            start_date = today - timedelta(days=today.weekday())
            records = records.filter(date_entered__gte=start_date)
        elif date_filter == 'month':
            records = records.filter(date_entered__month=today.month, date_entered__year=today.year)
        elif date_filter == 'quarter':
            # Simplified quarter calculation
            quarter = (today.month - 1) // 3 + 1
            start_month = 3 * (quarter - 1) + 1
            end_month = start_month + 2
            records = records.filter(
                date_entered__month__gte=start_month,
                date_entered__month__lte=end_month,
                date_entered__year=today.year
            )
        elif date_filter == 'year':
            records = records.filter(date_entered__year=today.year)
        elif date_filter == 'custom':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if start_date and end_date:
                records = records.filter(date_entered__range=[start_date, end_date])
    
    if sex_filter != 'all':
        records = records.filter(sex=sex_filter)
    
    if min_age:
        records = records.filter(age__gte=int(min_age))
    
    if max_age:
        records = records.filter(age__lte=int(max_age))
    
    if min_result:
        records = records.filter(result_value__gte=int(min_result))
    
    if max_result:
        records = records.filter(result_value__lte=int(max_result))
    
    if status_filter != 'all':
        records = records.filter(status=status_filter)
    
    # Calculate statistics
    total_records = records.count()
    high_vl_count = records.filter(result_value__gt=1000).count()
    iac_sessions_count = IacSession.objects.filter(hvl_record__in=records).count()
    resistance_tests_count = DrugResistanceApplication.objects.filter(hvl_record__in=records).count()
    
    # Prepare chart data
    # Viral Load Distribution
    viral_load_ranges = [
        ('<50', Q(result_value__lt=50)),
        ('50-199', Q(result_value__gte=50, result_value__lte=199)),
        ('200-999', Q(result_value__gte=200, result_value__lte=999)),
        ('1000-9999', Q(result_value__gte=1000, result_value__lte=9999)),
        ('≥10000', Q(result_value__gte=10000))
    ]
    
    viral_load_data = []
    viral_load_categories = []
    
    for label, query in viral_load_ranges:
        count = records.filter(query).count()
        viral_load_data.append(count)
        viral_load_categories.append(label)
    
    # Reason for Testing
    reason_counts = records.values('reason_for_test').annotate(count=Count('reason_for_test')).order_by('-count')
    reason_for_test_data = [item['count'] for item in reason_counts]
    reason_for_test_labels = [item['reason_for_test'] for item in reason_counts]
    
    # Drug Resistance Testing Status (last 6 months)
    resistance_months = []
    resistance_pending_data = []
    resistance_detected_data = []
    resistance_no_data = []
    
    today = timezone.now().date()
    for i in range(5, -1, -1):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_name = month_start.strftime('%b %Y')
        resistance_months.append(month_name)
        
        month_applications = DrugResistanceApplication.objects.filter(
            application_date__year=month_start.year,
            application_date__month=month_start.month
        )
        
        resistance_pending_data.append(month_applications.filter(resistance_detected='Pending').count())
        resistance_detected_data.append(month_applications.filter(resistance_detected='Yes').count())
        resistance_no_data.append(month_applications.filter(resistance_detected='No').count())
    
    # Recent records for the table
    recent_records = HVLRecord.objects.filter(iac_sessions__isnull=True).order_by('-date_entered')

    
    context = {
        'total_records': total_records,
        'high_vl_count': high_vl_count,
        'iac_sessions_count': iac_sessions_count,
        'resistance_tests_count': resistance_tests_count,
        'recent_records': recent_records.order_by('sn'),
        'viral_load_data': json.dumps(viral_load_data),
        'viral_load_categories': json.dumps(viral_load_categories),
        'reason_for_test_data': json.dumps(reason_for_test_data),
        'reason_for_test_labels': json.dumps(reason_for_test_labels),
        'resistance_pending_data': json.dumps(resistance_pending_data),
        'resistance_detected_data': json.dumps(resistance_detected_data),
        'resistance_no_data': json.dumps(resistance_no_data),
        'resistance_months': json.dumps(resistance_months),
    }
    
    return render(request, 'hvl_management/dashboard.html', context)


def collect_data(request):
    # Logic for collecting data goes here
    return render(request, 'hvl_management/collect_data.html')

def import_export(request):
    # Logic for import/export functionality goes here
    return render(request, 'hvl_management/import_export.html')

def notifications(request):
    # Logic for displaying notifications goes here
    return render(request, 'hvl_management/notifications.html')

def iac_sessions(request):
    # Logic for displaying IAC sessions goes here
    records = HVLRecord.objects.all()
    
    if request.method == 'POST':
        search_by = request.POST.get('search_by')
        query = request.POST.get('query')
        if search_by and query:
            if search_by == 'case_id':
                records = records.filter(sn=query)
            elif search_by == 'art_number':
                records = records.filter(art_number=query)
    
    context = {
        'recent_records': records
    }
    return render(request, 'hvl_management/iac_sessions.html', context)

def get_hvl_data(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    try:
        payload = json.loads(request.body)

        # Collect all HVLRecord objects
        hvl_records = []
        for item in payload:
            hvl_records.append(
                HVLRecord(
                    sn=item.get('SN'),
                    art_number=item.get('ART Number'),
                    sex=item.get('Sex'),
                    age=item.get('Age'),
                    date_entered=item.get('Date Entered'),
                    sample_log_number=item.get('Sample Log Number'),
                    reason_for_test=item.get('Reason for Test'),
                    result_value=item.get('Result Value'),
                )
            )

        # Bulk insert all at once
        HVLRecord.objects.bulk_create(hvl_records)

        return JsonResponse({'status': 'success', 'message': f'{len(hvl_records)} records inserted.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})