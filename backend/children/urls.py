from django.urls import path
from . import views

app_name = "children"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('children/', views.children_view, name='children'),
    path('children/add_child/', views.add_child, name='add_child'),
    path('reports/', views.reports, name='reports'),

    path('reminders/', views.reminders, name='reminders'),
    path('import-export/', views.import_export, name='import_export'),
    path('logs/', views.logs, name='logs'),

    path('children/child_dashboard/<str:hcc_number>/', views.child_dashboard_view, name='child_dashboard'),
    path('children/child_dashboard/<str:hcc_number>/edit/<str:field>/', views.edit_child_field_view, name='edit_field'),
    path('children/child_dashboard/<str:hcc_number>/add_visit/', views.add_visit, name='add_visit'),
    path('children/child_dashboard/<str:hcc_number>/add_hts/', views.add_hts_result, name='add_hts_result'),
    path('children/child_dashboard/<str:hcc_number>/update_outcome/', views.update_outcome, name='update_outcome'),
    path('children/child_dashboard/<str:hcc_number>/delete/', views.delete_child_view, name='delete_child'),
    path('children/child_dashboard/<str:hcc_number>/change_hcc/', views.change_hcc_number, name='change_hcc_number'),
    
    path('user-management/', views.user_management, name='user_management'),
    path('user-management/add/', views.add_user, name='add_user'),
    path('user-management/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('user-management/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('change-password/', views.change_password, name='change_password'),
    path('select-app/', views.app_selector, name='app_selector'),
]
