from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from pact.models import Patient

@login_required
def index(request):
    patients = Patient.objects.all()

    context = {
        'patients': patients
    }
    return render(request, 'art/index.html', context)
