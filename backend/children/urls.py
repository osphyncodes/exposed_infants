from django.urls import path
from . import views

app_name = "children"

urlpatterns = [
    path('exposed/dashboard/', views.dashboard, name='dashboard'),
    path('exposed/children/', views.children_view, name='children'),
    path('exposed/children/add_child/', views.add_child, name='add_child'),
    path('exposed/reports/', views.reports, name='reports'),

    path('exposed/reminders/', views.reminders, name='reminders'),
    path('exposed/import-export/', views.import_export, name='import_export'),
    path('exposed/logs/', views.logs, name='logs'),

    path('exposed/children/child_dashboard/<str:hcc_number>/', views.child_dashboard_view, name='child_dashboard'),
    path('exposed/children/child_dashboard/<str:hcc_number>/edit/<str:field>/', views.edit_child_field_view, name='edit_field'),
    path('exposed/children/child_dashboard/<str:hcc_number>/add_visit/', views.add_visit, name='add_visit'),
    path('exposed/children/child_dashboard/<str:hcc_number>/add_hts/', views.add_hts_result, name='add_hts_result'),
    path('exposed/children/child_dashboard/<str:hcc_number>/update_outcome/', views.update_outcome, name='update_outcome'),
    path('exposed/children/child_dashboard/<str:hcc_number>/delete/', views.delete_child_view, name='delete_child'),
    path('exposed/children/child_dashboard/<str:hcc_number>/change_hcc/', views.change_hcc_number, name='change_hcc_number'),
    
    path('user-management/', views.user_management, name='user_management'),
    path('user-management/add/', views.add_user, name='add_user'),
    path('user-management/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('user-management/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('change-password/', views.change_password, name='change_password'),
    path('select-app/', views.app_selector, name='app_selector'),
    path('', views.app_selector, name='app_selector')
]
