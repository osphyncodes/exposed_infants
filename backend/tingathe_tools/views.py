from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pact.models import Patient
from .models import ClientCard, ChildICT
from .forms import ClientCardForm, ChildICTForm

def tingathe_tools_index(request):
    return render(request, 'tingathe_tools/index.html')

# Client Card Views
def client_card_list(request):
    cards = ClientCard.objects.all().select_related('patient')
    return render(request, 'tingathe_tools/client_card/list.html', {'cards': cards})

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
def child_ict_list(request):
    mothers = Patient.objects.filter(
        gender='F', 
        age__gte=15, 
        art_status='ON_ART'
    ).prefetch_related('children')
    return render(request, 'tingathe_tools/child_ict/list.html', {'mothers': mothers})

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

def child_ict_delete(request, pk):
    child = get_object_or_404(ChildICT, pk=pk)
    if request.method == 'POST':
        child.delete()
        messages.success(request, 'Child record deleted successfully!')
    return redirect('tingathe_tools:child_ict_list')

def dashboard(request):
    # Statistics for dashboard
    total_cards = ClientCard.objects.count()
    in_progress_cards = ClientCard.objects.filter(status='IN_PROGRESS').count()
    completed_cards = ClientCard.objects.filter(status='COMPLETED').count()
    
    mothers_with_children = Patient.objects.prefetch_related('children').count()
    
    children_with_unknown_status = ChildICT.objects.filter(hiv_status='UNKNOWN').count()
    
    return render(request, 'tingathe_tools/dashboard.html', {
        'total_cards': total_cards,
        'in_progress_cards': in_progress_cards,
        'completed_cards': completed_cards,
        'mothers_with_children': mothers_with_children,
        'children_with_unknown_status': children_with_unknown_status,
    })