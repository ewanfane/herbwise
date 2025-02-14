from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('api/receive/', views.receive_data, name='receive_data'),
    path('poker/', views.roulette_view, name='poker'),
]
