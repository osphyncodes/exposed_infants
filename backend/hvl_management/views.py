import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import HVLRecord

def dashboard(request):
    return render(request, 'hvl_management/dashboard.html')

def collect_data(request):
    # Logic for collecting data goes here
    return render(request, 'hvl_management/collect_data.html')

def import_export(request):
    # Logic for import/export functionality goes here
    return render(request, 'hvl_management/import_export.html')

def notifications(request):
    # Logic for displaying notifications goes here
    return render(request, 'hvl_management/notifications.html')


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