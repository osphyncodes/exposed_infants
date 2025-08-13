from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pact.models import Patient
from .models import ClientCard, ChildICT
from .forms import ClientCardForm, ChildICTForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def tingathe_tools_index(request):
    return render(request, 'tingathe_tools/index.html')

# Client Card Views
@login_required
def client_card_list(request):
    cards = ClientCard.objects.all().select_related('patient')
    return render(request, 'tingathe_tools/client_card/list.html', {'cards': cards})

@csrf_exempt
def import_client_cards(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Check file extension
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        # Process the CSV file
        results = ClientCard.import_client_card(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

@login_required
def import_export(request):
    """
    Render the Pact import/export view.
    """
    return render(request, 'tingathe_tools/imports/import_export.html')

@login_required
def client_card_create(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = ClientCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.patient = patient
            card.save()
            messages.success(request, 'Client card created successfully!')
            return redirect('tingathe_tools:client_card_list')
    else:
        form = ClientCardForm()
    return render(request, 'tingathe_tools/client_card/create.html', {
        'form': form,
        'patient': patient
    })

@login_required
def client_card_update(request, pk):
    card = get_object_or_404(ClientCard, pk=pk)
    if request.method == 'POST':
        form = ClientCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client card updated successfully!')
            return redirect('tingathe_tools:client_card_list')
    else:
        form = ClientCardForm(instance=card)
    return render(request, 'tingathe_tools/client_card/update.html', {
        'form': form,
        'card': card
    })

# Child ICT Views
@login_required
def child_ict_list(request):
    mothers = Patient.objects.filter(
        gender='F', 
        age__gte=15, 
        art_status='ON_ART'
    ).prefetch_related('children')
    return render(request, 'tingathe_tools/child_ict/list.html', {'mothers': mothers})

@login_required
def child_ict_create(request, mother_id):
    mother = get_object_or_404(Patient, pk=mother_id)
    if request.method == 'POST':
        form = ChildICTForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.mother = mother
            child.save()
            messages.success(request, 'Child record added successfully!')
            return redirect('tingathe_tools:child_ict_list')
    else:
        form = ChildICTForm()
    return render(request, 'tingathe_tools/child_ict/create.html', {
        'form': form,
        'mother': mother
    })

@login_required
def child_ict_update(request, pk):
    child = get_object_or_404(ChildICT, pk=pk)
    if request.method == 'POST':
        form = ChildICTForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, 'Child record updated successfully!')
            return redirect('tingathe_tools:child_ict_list')
    else:
        form = ChildICTForm(instance=child)
    return render(request, 'tingathe_tools/child_ict/update.html', {
        'form': form,
        'child': child
    })

@login_required
def child_ict_delete(request, pk):
    child = get_object_or_404(ChildICT, pk=pk)
    if request.method == 'POST':
        child.delete()
        messages.success(request, 'Child record deleted successfully!')
    return redirect('tingathe_tools:child_ict_list')

@login_required
def dashboard(request):
    # Statistics for dashboard
    total_cards = ClientCard.objects.count()
    in_progress_cards = ClientCard.objects.filter(status='IN_PROGRESS').count()
    completed_cards = ClientCard.objects.filter(status='COMPLETED').count()

    mothers_with_children = ChildICT.objects.values('mother').distinct().count()
    
    children_with_unknown_status = ChildICT.objects.filter(hiv_status='UNKNOWN').count()

    return render(request, 'tingathe_tools/dashboard.html', {
        'total_cards': total_cards,
        'in_progress_cards': in_progress_cards,
        'completed_cards': completed_cards,
        'mothers_with_children': mothers_with_children,
        'children_with_unknown_status': children_with_unknown_status,
    })