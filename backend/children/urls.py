from django.urls import path
from . import views

app_name = "children"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('children/', views.children_views, name='children'),
    path('childrens/', views.children_view, name='childrens'),
    path('children/add_child/', views.add_child, name='add_child'),

    path('reminders/', views.reminders, name='reminders'),
    path('import-export/', views.import_export, name='import_export'),
    path('logs/', views.logs, name='logs'),

    path('children/child_dashboard/<str:hcc_number>/', views.child_dashboard_view, name='child_dashboard'),
    path('children/child_dashboard/<str:hcc_number>/edit/<str:field>/', views.edit_child_field_view, name='edit_field'),

    path('children/child_dashboard/<str:hcc_number>/add_visit/', views.add_visit, name='add_visit'),
    path('children/child_dashboard/<str:hcc_number>/view_visits/', views.view_child_visits, name='view_visits'),
    
    path('children/child_dashboard/<str:hcc_number>/add_hts/', views.add_hts_result, name='add_hts_result'),
    path('children/child_dashboard/<str:hts_id>/edit_hts/', views.edit_hts_result, name='edit_hts_result'),
    path('children/child_dashboard/<str:hcc_number>/view_hts/', views.view_hts_samples, name='view_hts_samples'),
    path('children/child_dashboard/delete_hts_result/<str:hts_id>/', views.delete_hts_sample, name='delete_hts_sample'),

    path('children/child_dashboard/<str:hcc_number>/update_outcome/', views.update_outcome, name='update_outcome'),
    path('children/child_dashboard/<str:hcc_number>/delete/', views.delete_child_view, name='delete_child'),
    path('children/child_dashboard/<str:hcc_number>/change_hcc/', views.change_hcc_number, name='change_hcc_number'),

    path('children/child_dashboard/delete-visit/<int:visit_id>/', views.delete_visit, name='delete_visit'),
    
    path('user-management/', views.user_management, name='user_management'),
    path('user-management/add/', views.add_user, name='add_user'),
    path('user-management/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('user-management/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('change-password/', views.change_password, name='change_password'),

    # Reports urls here
    path('reports/', views.reports, name='reports'),
    path("reports/defaulters", views.defaulters, name="defaulters"),
    path("reports/missed_appointment", views.missed, name="missed"),
    path('reports/defaulters/view', views.defaulters_view, name='defaulters_view'),

    path("reports/appointments", views.appointments, name="appointments"),
    path('reports/appointments/view', views.appointments_view, name='appointments_view'),

    path('missed-milestones/', views.missed_milestones_view, name='missed_milestones'),
    path('reports/eid_report/view/', views.eid_report, name='eid_report'),
]
