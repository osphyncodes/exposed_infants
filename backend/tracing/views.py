from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tracing.models import Tracing

@login_required
def dashboard(request):
    return render(request, 'tracing/dashboard.html')

@login_required
def import_export(request):
    return render(request, 'tracing/imports/import_export.html')

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
