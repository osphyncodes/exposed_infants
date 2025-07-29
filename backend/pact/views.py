from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from django.db.models import Count, Q, F, Value, IntegerField, Case, When
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Patient, LabResult, Regimen
from collections import defaultdict
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Now, Replace


@login_required
def reports(request):
    """
    Render the Pact reports view.
    """
    return render(request, 'pact/reports.html')

@login_required
def reminders(request):
    """
    Render the Pact reminders view.
    """
    return render(request, 'pact/reminders.html')

@login_required
def import_export(request):
    """
    Render the Pact import/export view.
    """
    return render(request, 'pact/import_export.html')

@login_required
def logs(request):
    """
    Render the Pact logs view.
    """
    return render(request, 'pact/logs.html')

@login_required
def user_management(request):
    """
    Render the Pact user management view.
    """
    return render(request, 'pact/user_management.html')

@login_required
def add_user(request):
    """
    Render the Pact add user view.
    """
    return render(request, 'pact/add_user.html')

@login_required
def edit_user(request, user_id):
    """
    Render the Pact edit user view.
    """
    return render(request, 'pact/edit_user.html', {'user_id': user_id})

@login_required
def delete_user(request, user_id):
    """
    Render the Pact delete user view.
    """
    return render(request, 'pact/delete_user.html', {'user_id': user_id})   

@login_required
def change_password(request):
    """
    Render the Pact change password view.
    """
    return render(request, 'pact/change_password.html')

@csrf_exempt
def import_patients(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Check file extension
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        # Process the CSV file
        results = Patient.import_from_csv(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

@csrf_exempt
def import_lab_results(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        results = LabResult.import_large_csv(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

def lab_import_view(request):
    return render(request, 'pact/imports/result_import.html')

@csrf_exempt
def import_patient_data(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'status': 'error',
                'message': 'Please upload a CSV file'
            }, status=400)
        
        results = Regimen.import_regimen_data(csv_file)
        
        return JsonResponse({
            'status': 'success',
            'results': results
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method or no file uploaded'
    }, status=400)

def import_view(request):
    return render(request, 'pact/imports/regimen.html')

def pact_dashboard(request):
    # 1. Total children < 20 years on ART
    children = Patient.objects.filter(outcome = 'On antiretrovirals').all()
    
    children_total = 0
    recent_count = 0
    suppressed_count = 0
    high_count = 0
    cons_high_total = 0


    high_vl_clients = []
    cons_high_vl_clients = []

    age_bands_high = defaultdict(int)
    age_bands_supp = defaultdict(int)
    age_bands_recent = defaultdict(int)

    gender_bands_high = defaultdict(int)
    gender_bands_supp = defaultdict(int)
    gender_bands_recent = defaultdict(int)

    for child in children:
        age = child.age()
        gender = child.gender
        cons_high_count = 0

        cons_results = {
            'result1': None,
            'result2': None,
            'result3': None
        }

        if age <= 19:
            #total children count
            children_total += 1

            arv_number = child.arv_number

            latest_result = child.results.order_by('-order_date').first()

            curr_results = child.results.filter(
                result__isnull = False
            ).order_by('-order_date').all()

            if curr_results.count() >= 3:
                curr_results = curr_results[:3]
                for curr_result in curr_results:
                    resultc = clean_string(curr_result.result)
                    if can_convert_to_int(resultc) and int(resultc) >= 1000 and cons_high_count <=3:
                        cons_high_count += 1

                        cons_results[f"result{cons_high_count}"] = f"Order Date: {curr_result.order_date}, Result: {resultc}"


                if cons_high_count == 3:
                    cons_high_total += 1
                    print(curr_result)
                    cons_high_vl_clients.append(childObject(child=child, result=curr_result, age=age, cons_results = cons_results))


            if latest_result and latest_result.result:
                # recent result count
                recent_count += 1
                ageBandDict(age_bands_recent, age)
                genderDict(gender_bands_recent, gender)

                result = latest_result.result
                result = clean_string(result)
                intvalue = can_convert_to_int(result)
                
                if intvalue:
                    if int(result)>= 1000:
                        high_count += 1
                        ageBandDict(age_bands_high, age)
                        genderDict(gender_bands_high, gender)
                        high_vl_clients.append(childObject(child=child, result=latest_result, age=age))
                    else:
                        suppressed_count += 1
                        ageBandDict(age_bands_supp, age)
                        genderDict(gender_bands_supp, gender)
                else:
                    if result.upper() == 'LDL':
                        suppressed_count += 1
                        ageBandDict(age_bands_supp,age)
                        genderDict(gender_bands_supp, gender)

    my_array = [i for i in high_vl_clients]
    items, paginator = paginate_array(request, my_array)

    my_array2 =[i for i in cons_high_vl_clients]
    items2, paginator2 = paginate_array(request, my_array2)

    context = {
        'children_on_art': children_total,
        'recent_vl_count': recent_count,
        'suppressed_vl': suppressed_count,
        'high_vl': high_count,
        'high_age_band': age_bands_high,
        'supp_age_band': age_bands_supp,
        'recent_age_band': age_bands_recent,
        'high_gender_band': gender_bands_high,
        'supp_gender_band': gender_bands_supp,
        'recent_gender_band': gender_bands_recent,
        'high_vl_clients': items,
        'cons_high': items2,
        'cons_high_count': cons_high_total
    }
    return render(request, 'pact/pact_dashboard.html', context)

def clean_string(input_string):
    # Remove <, >, and = characters from the string
    return input_string.replace('<', '').replace('>', '').replace('=', '')

def can_convert_to_int(input_string):
    try:
        int(input_string)  # Try to convert string to int
        return True
    except ValueError:  # If conversion fails, it raises a ValueError
        return False
    
def ageBandDict(dictionary, age):
    if 0 <= age <= 4:
        dictionary['0_4'] += 1
    elif 5 <= age <= 9:
        dictionary['5_9'] += 1
    elif 10 <= age <= 14:
        dictionary['10_14'] += 1
    elif 15 <= age <= 19:
        dictionary['15_19'] += 1
    
    return dictionary

def genderDict(dictionary, gender):
    if gender == 'Male':
        dictionary['male'] += 1
    elif gender == 'Female':
        dictionary['female'] += 1
    
    return dictionary

def childObject(child, result, age, cons_results = None):
    data = {
        'arv_number': child.arv_number,
        'age': age,
        'gender': child.gender,
        'order_date': result.order_date,
        'result': clean_string(result.result),
        'result_date': result.date_received,
        'cons_results': cons_results
    }
    return data

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_array(request, array, items_per_page=5):
    paginator = Paginator(array, items_per_page)
    page = request.GET.get('page')
    
    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        paginated_items = paginator.page(paginator.num_pages)
    
    return paginated_items, paginator

def children_view(request):
    children_list =  Patient.objects.under_age(20).filter(outcome = 'On antiretrovirals').all()
    

    childrens = []
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            children_list = children_list.filter(arv_number__icontains=query)
    

    # Get per_page from GET
    per_page = request.GET.get('per_page', '10')
    
    if per_page == 'all':
        page_obj = children_list  # Not paginated
        is_paginated = False
    else:
        try:
            per_page = per_page
        except ValueError:
            per_page = '10'
            # per_page = 10
        paginator = Paginator(children_list, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        is_paginated = True

    print(len(children_list))
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'is_paginated': is_paginated,
    }
    return render(request, 'pact/children.html', context)

def vl_status(result):
    if result:
        result = clean_string(result)
        if can_convert_to_int(result):
            if int(result) >= 1000:
                High = True
            else:
                High = False
        else:
            if result == 'LDL':
                High = False

        return High
    
def consHigh(resultArray):
    if resultArray and resultArray.count() >= 3:
        consCount = 0

        for result in resultArray[:3]:
            
            resultyo = clean_string(result.result)
            print(resultyo)
            if can_convert_to_int(resultyo):
                if int(resultyo) >= 1000:
                    consCount += 1


        if consCount == 3:
            return True
        else:
            return False
    

@login_required
def children_dashboard_view(request, art_number):
    child = get_object_or_404(Patient, arv_number=art_number)

    results = child.results.order_by('-order_date')
    recent_result = results.filter(result__isnull = False).first()
    result = recent_result.result
    status = vl_status(result)
    p = child.guardians.filter(type = 'Primary')
    s = child.guardians.filter(type = 'Secondary')

    consArray = results.filter(result__isnull = False)

    conshigh = consHigh(consArray)

    context = {
        'child': child,
        'age': child.age(),
        'regimen': child.regimens.first(),
        'p': p.first(),
        's': s.first(),
        'results': results.all(),
        'village': child.village.first(),
        'school': child.school.first(),
        'months_on_art': child.months_on_art(),
        'high': status,
        'recent_result': result,
        'surveys': child.surveys.all(),
        'conshigh': conshigh,
        'presentations': child.presentations.order_by('-presentation_date'),
        's_count': child.presentations.order_by('-presentation_date').count(),
        'genotypes':child.genotypes.all()

    }
    return render(request, 'pact/child_dashboard.html', context)
