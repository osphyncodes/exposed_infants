from django.http import JsonResponse
from django.views import View
from pact.models import Patient
from django.core.paginator import Paginator
from django.db import models

class PatientSearchAPI(View):
    def get(self, request):
        search_term = request.GET.get('q', '')
        
        patients = Patient.objects.filter(
            models.Q(arv_number__icontains=search_term) |
            models.Q(first_name__icontains=search_term) |
            models.Q(last_name__icontains=search_term)
        )[:30]  # Limit results
        
        results = [{
            'id': patient.id,
            'arv_number': patient.arv_number,
            'name': patient.full_name(),
            'age': patient.age(),
            'gender': patient.gender
        } for patient in patients]
        
        return JsonResponse({
            'results': results,
            'total_count': len(results)
        }, safe=False)

class PatientDetailAPI(View):
    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
            return JsonResponse({
                'id': patient.id,
                'arv_number': patient.arv_number,
                'name': patient.full_name(),
                'age': patient.age(),
                'gender': patient.gender
            })
        except Patient.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=404)