from django.urls import path
from . import views
from teen_club.api.views import PatientSearchAPI, PatientDetailAPI

app_name = 'sessions'

urlpatterns = [
    path('', views.SessionListView.as_view(), name='session_list'),
    path('dashboard/', views.session_dashboard, name='dashboard'),
    path('new/', views.SessionCreateView.as_view(), name='session_create'),
    path('<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('<int:pk>/edit/', views.SessionUpdateView.as_view(), name='session_update'),
    path('<int:session_id>/add-attendance/', views.add_attendance, name='add_attendance'),
    path('get-patient-details/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),
    path('api/patients/search/', PatientSearchAPI.as_view(), name='patient_search_api'),
    path('api/patients/<int:patient_id>/', PatientDetailAPI.as_view(), name='patient_detail_api'),
    path('search_name/api/', views.search_patient, name='search_name'),
]