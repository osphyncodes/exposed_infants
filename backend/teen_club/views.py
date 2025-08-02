from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from .models import Session, Attendance
from pact.models import Patient
from .forms import SessionForm, AttendanceForm
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import models

class SessionListView(ListView):
    model = Session
    template_name = 'sessions/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 10

class SessionDetailView(DetailView):
    model = Session
    template_name = 'teen_club/session_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.object
        attendances = session.attendances.select_related('patient')
        
        female_age_band = {
            'f': 0,
            's': 0,
            't': 0
        }

        male_age_band = {
            'f': 0,
            's': 0,
            't': 0
        }


        # Prepare data for charts
        purpose_data = {
            'Clinic': attendances.filter(purpose='Clinic').count(),
            'Support': attendances.filter(purpose='Support').count()
        }
        
        school_data = {
            'No': attendances.filter(school='No').count(),
            'YesDay': attendances.filter(school='Yes, Day').count(),
            'YesBRD': attendances.filter(school='Yes, BRD').count()
        }

        for att in attendances:
            age = att.patient.age()
            gender = att.patient.gender
            
            print(att.patient)
            if age <= 14:
                if gender == 'Male':
                    male_age_band['f'] += 1
                else:
                    female_age_band['f'] += 1
            elif age <= 18:
                if gender == 'Male':
                    male_age_band['s'] += 1
                else:
                    female_age_band['s'] += 1
            else:
                if gender == 'Male':
                    male_age_band['t'] += 1
                else:
                    female_age_band['t'] += 1
        
        context.update({
            'attendances': attendances,
            'purpose_data': purpose_data,
            'school_data': school_data,
            'new_patients': attendances.filter(new_in_teen=True).count(),
            'guardians_present': attendances.filter(guardian_present=True).count(),
            'vl_drawn': attendances.filter(vl_drawn=True).count(),
            'female': female_age_band,
            'male': male_age_band,
            'form': AttendanceForm()
        })

        return context
    

class SessionCreateView(CreateView):
    model = Session
    form_class = SessionForm
    template_name = 'teen_club/session_form.html'
    success_url = reverse_lazy('sessions:session_list')

class SessionUpdateView(UpdateView):
    model = Session
    form_class = SessionForm
    template_name = 'teen_club/session_form.html'
    success_url = reverse_lazy(':sessions:session_list')

@login_required
def add_attendance(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        art_number = request.POST.get('art_number')
        village = request.POST.get('village')
        new_in_teen = request.POST.get('new_in_teen')
        guardian_present = request.POST.get('guardian_present')
        vl_drawn = request.POST.get('vl_drawn')
        notes = request.POST.get('notes')
        purpose = request.POST.get('purpose')
        school = request.POST.get('school')

        patient = Patient.objects.filter(arv_number = art_number).first()
        if not patient:
            messages.info(request, 'Patient not found')
            return redirect('sessions:session_detail', pk = session.pk)
        # Check if patient already attended this session
        if Attendance.objects.filter(session=session, patient=patient).exists():
            messages.warning(request, 'This patient is already registered for this session!')
            return redirect('sessions:session_detail', pk = session.pk)
        else:
            attendance = Attendance(
                patient = patient,
                village = village,
                session = session,
                new_in_teen = True if new_in_teen == 'on' else False,
                guardian_present = True if guardian_present == 'on' else False,
                vl_drawn = True if vl_drawn == 'on' else False,
                notes = notes,
                purpose = purpose,
                school = school                  
            )


            attendance.save()
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('sessions:session_detail', pk = session.pk)
    
    return JsonResponse({'success': False})
@login_required
def get_patient_details(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    data = {
        'name': patient.full_name(),
        'age': patient.age(),
        'gender': patient.gender,
        'arv_number': patient.arv_number
    }
    return JsonResponse(data)

@login_required
def session_dashboard(request):
    # Get statistics for dashboard
    total_sessions = Session.objects.count()
    total_attendance = Attendance.objects.count()
    
    # Get recent sessions
    recent_sessions = Session.objects.order_by('-session_date')[:5]
    
    # Get attendance trends (last 6 months)
    # This would require a more complex query in a real implementation
    
    context = {
        'total_sessions': total_sessions,
        'total_attendance': total_attendance,
        'recent_sessions': recent_sessions
    }
    return render(request, 'teen_club/dashboard.html', context)

import json
@login_required
def search_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        art_number = data.get('art_number')
        if art_number != '':
            patient = Patient.objects.filter(arv_number = art_number).first()
        else:
            return JsonResponse({
                'status': 'success',
                'name': ''
            })

        if patient:
            name = patient.name

        if not patient:
            return JsonResponse({
                'status': 'success',
                'name': 'Not Found'
            })

        return JsonResponse({
                'status': 'success',
                'name': name
            })


