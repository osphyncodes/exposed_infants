from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import Patient, ChildVisit
from .forms import ChildVisitForm
import json
from django.http import JsonResponse

login_required
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        arv_number = data.get('arv_number')
        patient = Patient.objects.filter(arv_number = arv_number).first()

        if patient:
            results = patient.results.all().order_by('-order_date')[:2]
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

@login_required
def visit_stats(request):
    visits = ChildVisit.objects.all()

    context = {
        'visits': visits
    }
    return render(request, 'art/reports/visit_stats.html', context)

login_required
def patient_dashboard(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    form = ChildVisitForm()
    visits = patient.artvisits.all().order_by('-visit_date')
    return render(request, 'art/dashboard.html', {
        'patient': patient,
        'visits': visits,
        'form': form
    })

login_required
def add_visit(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = ChildVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            return redirect('art:patient_dashboard', patient_id=patient_id)
    else:
        form = ChildVisitForm()
    return render(request, 'art/partials/add_visit.html', {
        'form': form,
        'patient': patient
    })

login_required
def edit_visit(request, visit_id):
    visit = get_object_or_404(ChildVisit, pk=visit_id)
    if request.method == 'POST':
        form = ChildVisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard', patient_id=visit.patient_id)
    else:
        form = ChildVisitForm(instance=visit)
    return render(request, 'art/partials/edit_visit.html', {
        'form': form,
        'visit': visit
    })

login_required
def delete_visit(request, visit_id):
    visit = get_object_or_404(ChildVisit, pk=visit_id)
    patient_id = visit.patient_id
    visit.delete()
    return redirect('art:patient_dashboard', patient_id=patient_id)