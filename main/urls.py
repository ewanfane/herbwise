from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gardens/', views.gardens, name='gardens'),
    path('garden_details', views.garden_details, name='garden_details'),

    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('api/receive/', views.receive_data, name='receive_data'),
    path('latest_record/<int:plant_id>/', views.latest_record, name='latest_record'),

]
 