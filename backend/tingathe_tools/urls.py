from django.urls import path
from . import views

app_name = 'tingathe_tools'

urlpatterns = [
    path('', views.tingathe_tools_index, name='tingathe_tools_index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Client Card URLs
    path('client-cards/', views.client_card_list, name='client_card_list'),
    path('client-cards/create/<int:patient_id>/', views.client_card_create, name='client_card_create'),
    path('client-cards/update/<int:pk>/', views.client_card_update, name='client_card_update'),
    
    # Child ICT URLs
    path('child-ict/', views.child_ict_list, name='child_ict_list'),
    path('child-ict/create/<int:mother_id>/', views.child_ict_create, name='child_ict_create'),
    path('child-ict/update/<int:pk>/', views.child_ict_update, name='child_ict_update'),
    path('child-ict/delete/<int:pk>/', views.child_ict_delete, name='child_ict_delete'),
    path('import-export/', views.import_export, name='import_export'),
    path('api/import/', views.import_client_cards, name='api_client_cards'),
]
