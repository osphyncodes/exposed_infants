from django.urls import path
app_name = 'tracing'
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),   
    path('import', views.import_export, name='import_export'), 
    path('notifications', views.notifications, name='notifications'),
    path('api/tracing/', views.import_tracing_data, name='api_tracing'),
    path('updates/', views.tracing_updates, name='tracing_updates'),
    path('update-field/', views.update_tracing_field, name='update_tracing_field'),
    path('add-phone-tracing/', views.add_phone_tracing, name='add_phone_tracing'),
    path('add-home-tracing/', views.add_home_tracing, name='add_home_tracing'),
    path('tracing/<int:unique_id>/', views.tracing_detail, name='tracing_detail'),
    path('phone-tracing/delete/<int:pk>/', views.delete_phone_tracing, name='delete_phone_tracing'),
    path('home-tracing/delete/<int:pk>/', views.delete_home_tracing, name='delete_home_tracing'),
    path('import/attendance/', views.import_attendance_page, name='import_attendance_page'),
    path('api-refresh-attempts/', views.refresh_tracing_attempts, name='refresh_tracing_attempts')
]
