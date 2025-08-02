from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from pact.models import Patient
import json
from django.http import JsonResponse

def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arv_number = data.get('arv_number')
        patient = Patient.objects.filter(arv_number = arv_number).first()

        if patient:
            results = patient.results.all().order_by('-order_date')[:4]
            visits = patient.artvisits.all().order_by('-visit_date')

            data = {
                "order_date": list(results.values_list('order_date', flat=True)),
                "result": list(results.values_list('result', flat=True)),
                "date_received": list(results.values_list('date_received', flat=True)),
            }

            age = patient.age()
            months = patient.months_on_art()

            visits_array = []

            for v in visits:
                vis = {
                    'visit_date': v.visit_date,
                    'vl_draw': v.viral_load,
                    'regimen': v.regimen,
                    'arv_given': v.arv_given,
                    'next_appointment': v.next_outcome_date
                }
                visits_array.append(vis)

            data = {
                'patients': data,
                'visits': visits_array,
                'p': f"{arv_number}:{patient.name}, Gender: {patient.gender}, DOB: {patient.birthdate}({age}), DSA: {patient.art_start_date}({months})",
                'message':'Recieved'
            }

            return JsonResponse(data)
        data = {
            'p': 'Record Not Found'
        }
        return JsonResponse(data, safe=False)

    return render(request, 'art/index.html')
