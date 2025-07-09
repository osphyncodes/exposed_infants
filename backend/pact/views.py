from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def pact_dashboard(request):
    """
    Render the Pact dashboard.
    """
    return render(request, 'pact/pact_dashboard.html')

@login_required
def children_view(request):
    """
    Render the Pact children view.
    """
    return render(request, 'pact/children.html')

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
