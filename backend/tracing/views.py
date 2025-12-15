from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tracing.models import Tracing

from django.db.models import Count, Q, Case, When, IntegerField, F
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Tracing, Staff, HomeTracing, PhoneTracing
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
from io import StringIO
import csv
import re
from io import TextIOWrapper
from django.contrib import messages

@login_required
def refresh_tracing_attempts(request):

    tracings = Tracing.objects.all()

    for tracing in tracings:
        if tracing.home_tracings.count() > 0:
            tracing.home_traced = True
            tracing.tracing_attempted = True
        elif tracing.phone_tracings.count() > 0:
            tracing.phone_called = True
            tracing.tracing_attempted = True
        
        if tracing.home_tracings.filter(outcome='found_house_talked').exists() or tracing.phone_tracings.filter(outcome='talked_to_client').exists():
            tracing.tracing_outcome=True
            
        tracing.save()
    return redirect('tracing:tracing_updates')

@login_required
def tracing_updates(request):
    # Get filter parameters from request
    chw_filter = request.GET.get('chw', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    date_outcome_from = request.GET.get('date_outcome_from', '')
    date_outcome_to = request.GET.get('date_outcome_to', '')
    tracing_type = request.GET.get('type', '')
    outcome_filter = request.GET.getlist('outcome', '')
    with_phone_filter = request.GET.get('with_phone', '')
    home_traced_filter = request.GET.get('home_traced', '')
    tracing_attempted_filter = request.GET.get('tracing_attempted', '')
    talked_to_filter = request.GET.get('talked_to', '')
    
    # Start with all tracings
    tracings = Tracing.objects.all().select_related('chw').filter(date_entered__gte='2025-10-01')
    
    # Apply filters
    if chw_filter:
        tracings = tracings.filter(chw__id=chw_filter)
    
    if date_from:
        tracings = tracings.filter(date_entered__gte=date_from)
    
    if date_to:
        tracings = tracings.filter(date_entered__lte=date_to)

    if date_outcome_from:
        tracings = tracings.filter(outcome_date__gte=date_outcome_from)

    if date_outcome_to:
        tracings = tracings.filter(outcome_date__lte=date_outcome_to)
    
    if tracing_type:
        tracings = tracings.filter(reason=tracing_type)
    
    if outcome_filter:
    # Handle "Unknown" specially
        if "Unknown" in outcome_filter:
            # Outcomes excluding "Unknown"
            known_outcomes = [o for o in outcome_filter if o != "Unknown"]

            if known_outcomes:
                tracings = tracings.filter(
                    Q(final_outcome__in=known_outcomes) | Q(final_outcome=None)
                )
            else:
                tracings = tracings.filter(final_outcome=None)
        else:
            tracings = tracings.filter(final_outcome__in=outcome_filter)
    
    if with_phone_filter:
        if with_phone_filter == 'yes':
            tracings = tracings.filter(with_phone=True)
        elif with_phone_filter == 'no':
            tracings = tracings.filter(with_phone=False)
    
    if home_traced_filter:
        if home_traced_filter == 'yes':
            tracings = tracings.filter(home_traced=True)
        elif home_traced_filter == 'no':
            tracings = tracings.filter(home_traced=False)
    
    if tracing_attempted_filter:
        if tracing_attempted_filter == 'yes':
            tracings = tracings.filter(tracing_attempted = True)
        elif tracing_attempted_filter == 'no':
            tracings = tracings.filter(tracing_attempted = False)

    if talked_to_filter:
        if talked_to_filter == 'yes':
            tracings = tracings.filter(tracing_outcome = True)
        elif talked_to_filter == 'no':
            tracings = tracings.filter(tracing_outcome = False)

    print(f"this is chw filter{chw_filter}")
    # Get recent tracings
    recent_tracings = tracings.order_by('-date_entered')[:5]
    
    # Get all CHWs for filter dropdown
    all_chws = []
    for tracing in tracings:
        if tracing.chw not in all_chws:
            all_chws.append(tracing.chw)

    
    # Get unique values for filter dropdowns
    tracing_types = Tracing.objects.values_list('reason', flat=True).distinct()

    outcomes = ['Unknown']
    outcomes_list = Tracing.objects.values_list('final_outcome', flat=True).distinct()

    for outcome in outcomes_list:
        if outcome != '':
            if outcome != None:
                outcomes.append(outcome)
    
    context = {
        'tracings': tracings.order_by('unique_id', 'chw__name'),
        'recent_tracings': recent_tracings,
        'all_chws': all_chws,
        'tracing_types': tracing_types,
        'outcomes': outcomes,
        'chw_filter': chw_filter,
        'date_from': date_from,
        'date_to': date_to,
        'tracing_type': tracing_type,
        'outcome_filter': outcome_filter,
        'with_phone_filter': with_phone_filter,
        'home_traced_filter': home_traced_filter,
        'tracing_attempted_filter': tracing_attempted_filter,
        'talked_to_filter': talked_to_filter,
        'date_outcome_from': date_outcome_from,
        'date_outcome_to': date_outcome_to,
    }
    
    return render(request, 'tracing/tracing_updates.html', context)


def filters(request):
    chw_filter = request.GET.get('chw', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    date_outcome_from = request.GET.get('date_outcome_from', '')
    date_outcome_to = request.GET.get('date_outcome_to', '')
    tracing_type = request.GET.get('type', '')
    outcome_filter = request.GET.get('outcome', '')
    with_phone_filter = request.GET.get('with_phone', '')
    home_traced_filter = request.GET.get('home_traced', '')
    
    # Start with all tracings
    tracings = Tracing.objects.all().select_related('chw')
    
    # Apply filters
    if chw_filter:
        tracings = tracings.filter(chw__id=chw_filter)
    
    if date_from:
        tracings = tracings.filter(date_entered__gte=date_from)
    
    if date_to:
        tracings = tracings.filter(date_entered__lte=date_to)
    
    if tracing_type:
        tracings = tracings.filter(reason=tracing_type)
    
    if date_outcome_from:
        tracings = tracings.filter(outcome_date__gte=date_outcome_from)

    if date_outcome_to:
        tracings = tracings.filter(outcome_date__lte=date_outcome_to)

    if outcome_filter:
        tracings = tracings.filter(final_outcome=outcome_filter)
    
    if with_phone_filter:
        if with_phone_filter == 'yes':
            tracings = tracings.filter(with_phone=True)
        elif with_phone_filter == 'no':
            tracings = tracings.filter(with_phone=False)
    
    if home_traced_filter:
        if home_traced_filter == 'yes':
            tracings = tracings.filter(home_traced=True)
        elif home_traced_filter == 'no':
            tracings = tracings.filter(home_traced=False)
    
    return tracings, chw_filter, date_from, date_to, date_outcome_from, date_outcome_to, tracing_type, outcome_filter, with_phone_filter, home_traced_filter

@login_required
def dashboard(request):
    # Get filter parameters from request
    tracings, chw_filter, date_from, date_to, date_outcome_from, date_outcome_to, tracing_type, outcome_filter, with_phone_filter, home_traced_filter = filters(request)

    
    # Calculate statistics
    total_tracings = tracings.count()
    with_phone_count = tracings.filter(with_phone=True).count()
    home_traced_count = tracings.filter(home_traced=True).count()
    successful_tracings = tracings.filter(tracing_outcome=True).count()
    
    # Get outcome distribution
    outcome_distribution = tracings.values('final_outcome').annotate(
        count=Count('final_outcome')
    ).order_by('-count')
    
    # Get tracing type distribution
    type_distribution = tracings.values('reason').annotate(
        count=Count('reason')
    ).order_by('-count')


    # Get CHW performance
    chw_performance = tracings.values(
        'chw__chw_code',
        'chw__name'
    ).annotate(
        tracing_count=Count('unique_id', distinct=True),
        with_phone_count=Count(
            Case(
                When(with_phone=True, then=1),
                output_field=IntegerField()
            )
        ),
        number_called=Count(
            Case(
                When(phone_tracings__isnull=False, then=F('unique_id')),
                output_field=IntegerField()
            ),
            distinct=True
        ),
        home_traced_count=Count(
            Case(
                When(home_tracings__isnull=False, then=F('unique_id')),
                output_field=IntegerField()
            ),
            distinct=True
        ),
        success_count=Count(
            Case(
            When(
                Q(home_tracings__id__isnull=False) |
                Q(phone_tracings__id__isnull=False),
                then=F('unique_id')  # count distinct Tracing IDs
            ),
            output_field=IntegerField()
        ),
        distinct=True
        )
    ).order_by('-tracing_count')


    reason_performance = tracings.values('reason').annotate(
        # base total per reason (distinct tracings)
        tracing_count=Count('unique_id', distinct=True),

        # how many tracings have a phone recorded
        with_phone_count=Count(
            'unique_id',
            filter=Q(with_phone=True),
            distinct=True
        ),
        
        talked_to=Count(
            'unique_id',
            filter=Q(tracing_outcome=True),
            distinct=True
        ),
        # how many tracings have at least one phone call (any outcome)
        number_called=Count(
            'unique_id',
            filter=Q(phone_tracings__isnull=False),
            distinct=True
        ),

        # how many tracings have at least one home tracing (any outcome)
        home_traced_count=Count(
            'unique_id',
            filter=Q(home_tracings__isnull=False),
            distinct=True
        ),

        # success = has any phone call OR any home tracing (regardless of outcome)
        success_count=Count(
            'unique_id',
            filter=Q(phone_tracings__isnull=False) | Q(home_tracings__isnull=False),
            distinct=True
        ),
    ).order_by('-tracing_count')

    
    # Get recent tracings
    recent_tracings = tracings.order_by('-date_entered')[:5]
    
    # Get all CHWs for filter dropdown
    all_chws = Staff.objects.all().filter(id__gt=3)
    
    # Get unique values for filter dropdowns
    tracing_types = Tracing.objects.values_list('reason', flat=True).distinct()
    outcomes = Tracing.objects.values_list('final_outcome', flat=True).distinct()
    
    context = {
        'tracings': tracings,
        'total_tracings': total_tracings,
        'with_phone_count': with_phone_count,
        'home_traced_count': home_traced_count,
        'successful_tracings': successful_tracings,
        'outcome_distribution': outcome_distribution,
        'type_distribution': type_distribution,
        'chw_performance': chw_performance,
        'recent_tracings': recent_tracings,
        'all_chws': all_chws,
        'tracing_types': tracing_types,
        'outcomes': outcomes,
        'chw_filter': chw_filter,
        'date_from': date_from,
        'date_to': date_to,
        'date_outcome_from': date_outcome_from,
        'date_outcome_to': date_outcome_to,
        'tracing_type': tracing_type,
        'outcome_filter': outcome_filter,
        'with_phone_filter': with_phone_filter,
        'home_traced_filter': home_traced_filter,
        'reason_performance': reason_performance
    }
    
    return render(request, 'tracing/dashboard.html', context)

@login_required
def import_export(request):
    return render(request, 'tracing/imports/import_export.html')

@login_required
def notifications(request):
    return render(request, 'tracing/notifications.html')

@csrf_exempt
def import_tracing_data(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        results = Tracing.import_tracing_csv(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

@require_POST
@csrf_exempt
def update_tracing_field(request):
    try:
        data = json.loads(request.body)
        tracing_id = data.get('tracing_id')
        field = data.get('field')
        value = data.get('value')
 
        
        tracing = Tracing.objects.get(unique_id=tracing_id)
        
        if field == 'outcome_date':
            if value.strip() == '':
               value = None
            
            if tracing.final_outcome.strip() == '' and value is not None: 
                return JsonResponse({'success': False, 'error': 'Set final outcome before setting outcome date'})
        
        if field == 'final_outcome':
            if value.strip() == '':
                Tracing.objects.filter(unique_id=tracing_id).update(outcome_date=None)
                tracing.refresh_from_db()
                value = None

        if isInteger(field):
            chw = Tracing.objects.filter(name=value)
            print(f"This is the value {value}")
            tracing.chw = chw
            tracing.save()
            return JsonResponse({'success': True})
        
        # Update the field
        if hasattr(tracing, field):
            setattr(tracing, field, value)
            if field != 'tracing_updated':
                setattr(tracing, 'tracing_updated', False)

            tracing.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid field'})
            
    except Tracing.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tracing record not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def add_phone_tracing(request):
    try:
        tracing_id = request.POST.get('tracing_id')
        date_called = request.POST.get('date_called')
        outcome = request.POST.get('outcome')
        notes = request.POST.get('notes', '')
        
        tracing = Tracing.objects.get(unique_id=tracing_id)

        if tracing.phone_tracings.filter(date_called=date_called).exists():
            return JsonResponse({'success': False, 'error': 'A phone tracing for this date already exists.'})
        # Create phone tracing record

        if tracing.phone_tracings.count() >= 3:
            return JsonResponse({'success': False, 'error': 'Maximum of 3 phone tracing attempts reached.'})

        # Create phone tracing record
        PhoneTracing.objects.create(
            tracing=tracing,
            date_called=date_called,
            outcome=outcome,
            notes=notes
        )

        tracing.tracing_updated = False
        tracing.tracing_attempted = True
        tracing.home_traced = True
        

        if outcome == 'talked_to_client':
            talking_to_client = True
            tracing.tracing_outcome = True
        else:
            talking_to_client = False

        tracing.save()

        return JsonResponse({
            'success': True,
            'talking_to_client': talking_to_client
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def add_home_tracing(request):
    try:
        tracing_id = request.POST.get('tracing_id')
        date_visited = request.POST.get('date_visited')
        outcome = request.POST.get('outcome')
        notes = request.POST.get('notes', '')
        
        # try:
        #     # Convert string (YYYY-MM-DD) to a date object
        #     date_visited = datetime.strptime(date_visited, "%Y-%m-%d").date()
        # except (TypeError, ValueError):
        #     return JsonResponse({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD.'})

        # # Now you can safely compare
        # if date_visited > timezone.now().date():
        #     return JsonResponse({'success': False, 'error': 'Date visited cannot be in the future.'})
                
        tracing = Tracing.objects.get(unique_id=tracing_id)
        
        if tracing.home_tracings.filter(date_visited=date_visited).exists():
            return JsonResponse({'success': False, 'error': 'A home tracing for this date already exists.'})
        # Create home tracing record

        if tracing.home_tracings.count() >= 2:
            return JsonResponse({'success': False, 'error': 'Maximum of 2 home tracing attempts reached.'})
    
        HomeTracing.objects.create(
            tracing=tracing,
            date_visited=date_visited,
            outcome=outcome,
            notes=notes
        )

        tracing.tracing_updated = False
        tracing.tracing_attempted = True
        tracing.home_traced = True
         

        if outcome == 'found_house_talked':
            talking_to_client = True
            tracing.tracing_outcome = True
        else:
            talking_to_client = False

        tracing.save()

        return JsonResponse({
            'success': True,
            'talking_to_client': talking_to_client
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@login_required
def tracing_detail(request, unique_id):
    tracing = get_object_or_404(Tracing, unique_id=unique_id)
    phone_attempts = PhoneTracing.objects.filter(tracing=tracing).order_by('-date_called')
    home_attempts = HomeTracing.objects.filter(tracing=tracing).order_by('-date_visited')
    
    context = {
        'tracing': tracing,
        'phone_attempts': phone_attempts,
        'home_attempts': home_attempts,
    }
    
    return render(request, 'tracing/tracing_detail.html', context)

@login_required
def delete_phone_tracing(request, pk):
    phone_tracing = get_object_or_404(PhoneTracing, pk=pk)
    tracing_id = phone_tracing.tracing.unique_id
    phone_tracing.delete()
    return redirect('tracing:tracing_detail', unique_id=tracing_id)

@login_required
def delete_home_tracing(request, pk):
    home_tracing = get_object_or_404(HomeTracing, pk=pk)
    tracing_id = home_tracing.tracing.unique_id
    home_tracing.delete()
    return redirect('tracing:tracing_detail', unique_id=tracing_id)

def isInteger(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

@login_required
def collect_data(request):
    # Logic for collecting data goes here
    return render(request, 'tracing/collect_data.html')

@login_required
def get_hvl_data(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    try:
        payload = json.loads(request.body)

        # Collect all Tracing objects
        tracing_records = []
        for item in payload:
            tracing_records.append(
                Tracing(
                    unique_id=item.get('Unique ID'),
                    date_entered=item.get('Date Entered'),
                    chw = Staff.objects.get(id=item.get('CHW')) if item.get('CHW') else None,
                    art_number=item.get('ART Number'),
                    name = item.get('Name'),
                    gender=item.get('Gender'),
                    age=item.get('Age'),
                    phone_number=item.get('Phone Number'),
                    type=item.get('Type'),
                    reason=item.get('Reason'),
                    # true if yes, false if no
                    with_phone=(item.get('With Phone', '').lower() == 'yes'),
                )
            )

        # Bulk insert all at once
        Tracing.objects.bulk_create(tracing_records)

        return JsonResponse({'status': 'success', 'message': f'{len(tracing_records)} records inserted.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@login_required
def import_attendance_page(request):
    if request.method == 'POST':
        
        if request.FILES.get('csvFile'):
            csv_file = request.FILES['csvFile']

            if not csv_file.name.endswith('.csv'):
                return redirect('tracing:import_attendance')
            
        

            # Read entire file into memory
            content = TextIOWrapper(csv_file.file, encoding='utf-8', newline='').read()
            
            # First pass to get all unique_ids for the query
            reader = csv.DictReader(StringIO(content))
            count = 0

            try:
                for row in reader:
                    arv_number = extract_art_number(row['ARV Number'])
                    visit_date = to_yyyy_mm_dd(row['Visit date'])

                    tracing = Tracing.objects.filter(art_number=arv_number, type='ART').first()

                    if tracing:
                        
                        if (tracing.final_outcome == None or tracing.final_outcome == '') and tracing.tracing_attempted:
                            tracing.final_outcome = "Attended Appointment"
                            tracing.outcome_date = visit_date

                            count += 1
                            tracing.save()

                        elif (tracing.final_outcome == None or tracing.final_outcome == '') and not tracing.tracing_attempted:
                            tracing.final_outcome = 'Came Back'
                            tracing.outcome_date = visit_date
                            count += 1
                            tracing.save()

                        child = Tracing.objects.filter(mother_art=arv_number).first()
                        if child:
                            print(f"Found tracing for ART number {arv_number}")
                            if (child.final_outcome == None or child.final_outcome == '') and child.tracing_attempted:
                                child.final_outcome = "Attended Appointment"
                                child.outcome_date = visit_date
                                count += 1
                                child.save()
                            else:
                                child.final_outcome = "Came Back"
                                child.outcome_date = visit_date
                                count += 1
                                child.save()

                messages.success(request, f"{count} Clients have been updated successfully!")
                return redirect('tracing:dashboard')
            
            except KeyError as e:
                messages.error(request, f"Missing expected column in CSV: {str(e)}")
                return redirect('tracing:import_attendance_page')

    return render(request, 'tracing/imports/attendance.html')


def extract_art_number(value: str) -> int | None:
    """
    Extract ART number from a string formatted like 'LGWN-ARV-234'.
    Returns the number as int, or None if not found.
    """
    match = re.search(r'(\d+)$', value)  # match digits at the end
    if match:
        return int(match.group(1))
    return None   

from datetime import datetime
from dateutil import parser

def to_yyyy_mm_dd(date_str: str) -> str | None:
    """
    Convert any date string to 'YYYY-MM-DD' format.
    Returns None if parsing fails.
    """
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def get_chws_data(request):
    chws = Staff.objects.filter(id__gt=3).values('id', 'name', 'chw_code')
    chw_list = list(chws)
    return JsonResponse({'chws': chw_list})