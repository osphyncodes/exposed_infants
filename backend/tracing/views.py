from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tracing.models import Tracing

from django.db.models import Count, Q, Case, When, IntegerField, F
from django.utils import timezone
from datetime import timedelta
from .models import Tracing, Staff, HomeTracing, PhoneTracing
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def tracing_updates(request):
    # Get filter parameters from request
    chw_filter = request.GET.get('chw', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
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

    
    # Get recent tracings
    recent_tracings = tracings.order_by('-date_entered')[:5]
    
    # Get all CHWs for filter dropdown
    all_chws = Staff.objects.all().filter(id__gt=3)
    
    # Get unique values for filter dropdowns
    tracing_types = Tracing.objects.values_list('reason', flat=True).distinct()
    outcomes = Tracing.objects.values_list('final_outcome', flat=True).distinct()
    
    context = {
        'tracings': tracings,
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
    }
    
    return render(request, 'tracing/tracing_updates.html', context)

@login_required
def dashboard(request):
    # Get filter parameters from request
    chw_filter = request.GET.get('chw', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
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
        
        # Update the field
        if hasattr(tracing, field):
            setattr(tracing, field, value)
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
        
        # Create phone tracing record
        PhoneTracing.objects.create(
            tracing=tracing,
            date_called=date_called,
            outcome=outcome,
            notes=notes
        )

        if outcome == 'talked_to_client':
            talking_to_client = True
        else:
            talking_to_client = False

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
        
        tracing = Tracing.objects.get(unique_id=tracing_id)
        
        # Create home tracing record
        HomeTracing.objects.create(
            tracing=tracing,
            date_visited=date_visited,
            outcome=outcome,
            notes=notes
        )

        if outcome == 'found_house_talked':
            talking_to_client = True
        else:
            talking_to_client = False

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